const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
module.exports=async({evaluate,navigate,until,web})=>{
    const statePath=path.resolve(web,'../.local/sync-state.json');
    const state=JSON.parse(fs.readFileSync(statePath,'utf8'));
    const accounts=JSON.parse(fs.readFileSync(path.resolve(web,'../.local/liceomap_preoficial_test.accounts.json'),'utf8'));
    const user=accounts.find(a=>a.rut==='20100002-5');
    await navigate();
    await until(()=>evaluate("document.querySelector('#app-preloader').hidden"),'intro');
    await evaluate(`document.querySelector('#btn-open-admin').click();document.querySelector('#admin-rut').value=${JSON.stringify(user.rut)};document.querySelector('#admin-pass').value=${JSON.stringify(user.password)};document.querySelector('#admin-login-form').requestSubmit()`);
    await until(()=>evaluate("!document.querySelector('#admin-dashboard').hidden && document.querySelector('#announcement-list-status').textContent.includes('anuncio(s)')"),'authorized list');
    if(state.action==='create') {
        const existing = await evaluate(`[...document.querySelectorAll('.announcement-item')].find(n=>n.querySelector('h4').textContent===${JSON.stringify(state.title)})?.dataset.announcementId`);
        if (existing) {
            state.id=existing;
            fs.writeFileSync(statePath,JSON.stringify(state));
            await evaluate("document.querySelector('#btn-logout-admin').click()");
            return;
        }
        await evaluate(`document.querySelector('#demo-announcement-title').value=${JSON.stringify(state.title)};document.querySelector('#demo-announcement-body').value='Publicación de prueba de sincronización WEB API Android';document.querySelector('#announcement-form').requestSubmit()`);
        await until(()=>evaluate("!document.querySelector('#announcement-save').disabled"),'saved');
        assert.equal(await evaluate("document.querySelector('#announcement-status').textContent"),'Anuncio publicado.');
        state.id=await evaluate(`[...document.querySelectorAll('.announcement-item')].find(n=>n.querySelector('h4').textContent===${JSON.stringify(state.title)}).dataset.announcementId`);
    } else if(state.action==='edit') {
        await evaluate(`document.querySelector('[data-announcement-id="${state.id}"] button').click();document.querySelector('#demo-announcement-title').value=${JSON.stringify(state.title+' editado')};document.querySelector('#announcement-form').requestSubmit()`);
        await until(()=>evaluate("!document.querySelector('#announcement-save').disabled"),'edited');
        assert.equal(await evaluate("document.querySelector('#announcement-status').textContent"),'Cambios guardados.');
    } else if(state.action==='withdraw') {
        await evaluate(`window.confirm=()=>true;document.querySelectorAll('[data-announcement-id="${state.id}"] button')[1].click()`);
        await until(()=>evaluate(`!document.querySelector('[data-announcement-id="${state.id}"] button')`),'withdrawn');
    } else throw Error('Unsupported sync action');
    fs.writeFileSync(statePath,JSON.stringify(state));
    await evaluate("document.querySelector('#btn-logout-admin').click()");
    console.log('PASS: browser synchronization action '+state.action);
};
