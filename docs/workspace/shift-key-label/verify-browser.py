import asyncio,base64,json,os,re,signal,subprocess,tempfile,time
from pathlib import Path
from websockets.asyncio.client import connect
root=Path(__file__).resolve().parents[3];out=root/'docs/workspace/shift-key-label';html=(root/'web/index.html').read_text();html=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',html,flags=re.I);html=re.sub(r'<link\b[^>]*>','',html,flags=re.I);html=html.replace('</head>','<style>'+(root/'web/app.css').read_text()+'</style></head>');nav=(root/'web/js/nav.js').read_text()
async def verify(profile,process):
 active=Path(profile)/'DevToolsActivePort'
 for _ in range(100):
  if active.exists():break
  await asyncio.sleep(.1)
 lines=active.read_text().splitlines()
 async with connect('ws://127.0.0.1:'+lines[0]+lines[1],proxy=None,max_size=10000000) as ws:
  i=0;errors=[]
  async def call(method,params=None,session=None):
   nonlocal i
   i+=1;msg={'id':i,'method':method,'params':params or {}}
   if session:msg['sessionId']=session
   await ws.send(json.dumps(msg))
   while True:
    r=json.loads(await asyncio.wait_for(ws.recv(),timeout=20))
    if r.get('method')=='Runtime.exceptionThrown':errors.append(r['params']['exceptionDetails'].get('text'))
    if r.get('id')==i:
     assert 'error' not in r,r
     return r.get('result',{})
  target=await call('Target.createTarget',{'url':'about:blank'});session=(await call('Target.attachToTarget',{'targetId':target['targetId'],'flatten':True}))['sessionId']
  await call('Runtime.enable',session=session);await call('Page.enable',session=session)
  async def evaluate(expr):
   r=await call('Runtime.evaluate',{'expression':expr,'returnByValue':True},session);assert 'exceptionDetails' not in r,r
   return r['result'].get('value')
  reports=[]
  for width,height in [(390,844),(360,800)]:
   await call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':True},session)
   await call('Page.navigate',{'url':'about:blank'},session);await asyncio.sleep(.1)
   frame=(await call('Page.getFrameTree',session=session))['frameTree']['frame']['id']
   await call('Page.setDocumentContent',{'frameId':frame,'html':html},session)
   await evaluate('window.positionHistoryPanel=()=>{};window.savedUrl=null;window.showSetup=()=>{};'+nav+'\nwindow.__sent=[]; window.sendKeys=(keys)=>window.__sent.push(keys);document.getElementById("terminalView").classList.add("active");document.getElementById("termKeys").style.display="";document.getElementById("termTitle").textContent="Keys · 隔离验证";document.getElementById("termContent").textContent="Shift + Tab 组合键验证，不连接真实 Agent";')
   await evaluate("document.getElementById('modShift').click()")
   assert await evaluate("document.getElementById('modShift').classList.contains('armed')")
   await evaluate("document.querySelector('[onclick=\"fireKey(\\'Tab\\')\"]').click()")
   assert await evaluate("keyQueue[0]")=='shift+Tab'
   report=json.loads(await evaluate("JSON.stringify({width:innerWidth,bodyWidth:document.body.scrollWidth,shiftLabel:document.getElementById('modShift').textContent,buttonWidth:document.getElementById('modShift').getBoundingClientRect().width,buttonScroll:document.getElementById('modShift').scrollWidth,buttonClient:document.getElementById('modShift').clientWidth,queued:keyQueue.slice()})"))
   assert report['width']==report['bodyWidth'] and report['shiftLabel']=='Shift' and report['buttonScroll']==report['buttonClient'],report
   screenshot=await call('Page.captureScreenshot',{'format':'png'},session);(out/('keys-'+str(width)+'.png')).write_bytes(base64.b64decode(screenshot['data']))
   await evaluate("document.querySelector('#keyQueueStrip button[onclick=\"sendQueuedKeys()\"]').click()")
   assert await evaluate("JSON.stringify(window.__sent)")=='[["shift+Tab"]]'
   assert await evaluate('keyQueue.length')==0
   reports.append(report)
  assert not errors,errors
  result={'viewports':reports,'combination':'Shift -> Tab -> Send captured shift+Tab','real_agent_input':False,'javascript_exceptions':errors}
  (out/'browser-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
with tempfile.TemporaryDirectory(prefix='herdr-shift-') as profile:
 process=subprocess.Popen(['/usr/bin/google-chrome','--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking','--remote-debugging-port=0','--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
 try:asyncio.run(verify(profile,process))
 finally:
  try:os.killpg(process.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:process.wait(timeout=10)
  except subprocess.TimeoutExpired:process.kill();process.wait()
  time.sleep(1)
