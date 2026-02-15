const PWAManager={SW_URL:'/static/js/sw.js',init(){if(!('serviceWorker'in navigator)){console.log('[PWA] 当前浏览器不支持 Service Worker');return;}
this.registerSW();this.setupUpdateListener();},registerSW(){navigator.serviceWorker.register(this.SW_URL,{scope:'/'}).then((registration)=>{console.log('[PWA] Service Worker 注册成功:',registration.scope);this.checkForUpdates(registration);}).catch((error)=>{console.error('[PWA] Service Worker 注册失败:',error);});},checkForUpdates(registration){setInterval(()=>{registration.update();},60*60*1000);},setupUpdateListener(){navigator.serviceWorker.addEventListener('controllerchange',()=>{console.log('[PWA] 新的 Service Worker 已激活');window.location.reload();});navigator.serviceWorker.addEventListener('message',(event)=>{if(event.data&&event.data.type==='UPDATE_AVAILABLE'){this.showUpdatePrompt();}});},showUpdatePrompt(){const updateBanner=document.createElement('div');updateBanner.className='update-banner';updateBanner.innerHTML=`
            <div class="update-banner-content">
                <span>🔄 发现新版本</span>
                <div class="update-banner-actions">
                    <button class="btn btn-sm btn-primary" id="updateNowBtn">立即更新</button>
                    <button class="btn btn-sm btn-outline-light" id="updateLaterBtn">稍后</button>
                </div>
            </div>
        `;updateBanner.style.cssText=`
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 20px;
            z-index: 9999;
            box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
            transform: translateY(100%);
            transition: transform 0.3s ease;
        `;document.body.appendChild(updateBanner);setTimeout(()=>{updateBanner.style.transform='translateY(0)';},100);document.getElementById('updateNowBtn').addEventListener('click',()=>{this.skipWaiting();updateBanner.style.transform='translateY(100%)';setTimeout(()=>updateBanner.remove(),300);});document.getElementById('updateLaterBtn').addEventListener('click',()=>{updateBanner.style.transform='translateY(100%)';setTimeout(()=>updateBanner.remove(),300);});},skipWaiting(){if(navigator.serviceWorker.controller){navigator.serviceWorker.controller.postMessage({type:'SKIP_WAITING'});}},clearCache(){if(navigator.serviceWorker.controller){navigator.serviceWorker.controller.postMessage({type:'CLEAR_CACHE'});}},showInstallPrompt(){window.addEventListener('beforeinstallprompt',(e)=>{e.preventDefault();this.deferredPrompt=e;this.showInstallButton();});},showInstallButton(){const installBtn=document.createElement('button');installBtn.className='btn btn-sm btn-outline-light';installBtn.innerHTML='📱 安装应用';installBtn.onclick=()=>{if(this.deferredPrompt){this.deferredPrompt.prompt();this.deferredPrompt.userChoice.then((result)=>{if(result.outcome==='accepted'){console.log('[PWA] 用户接受安装');}else{console.log('[PWA] 用户拒绝安装');}
this.deferredPrompt=null;installBtn.remove();});}};const navbarActions=document.querySelector('.navbar .ms-auto');if(navbarActions){navbarActions.insertBefore(installBtn,navbarActions.firstChild);}},isPWA(){return window.matchMedia('(display-mode: standalone)').matches||window.navigator.standalone===true;},getNetworkStatus(){if(navigator.onLine){return'online';}
return'offline';}};if(typeof module!=='undefined'&&module.exports){module.exports=PWAManager;}
if(typeof window!=='undefined'){if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',()=>{PWAManager.init();PWAManager.showInstallPrompt();});}else{PWAManager.init();PWAManager.showInstallPrompt();}
window.addEventListener('online',()=>{console.log('[PWA] 网络已连接');document.body.classList.remove('offline-mode');});window.addEventListener('offline',()=>{console.log('[PWA] 网络已断开');document.body.classList.add('offline-mode');});window.PWAManager=PWAManager;}
