// Compare against the actual source commit, not newly approved snapshots.
const {execFileSync}=require('node:child_process');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const read=file=>fs.readFileSync(path.join(root,file),'utf8').replace(/\r\n/g,'\n');
const original=file=>execFileSync('git',['show','5f2308a:'+file],{cwd:root,encoding:'utf8'}).replace(/\r\n/g,'\n');
for(const file of ['web/story.js','web/purpose.js','web/finale.js','web/style.css','web/purpose.css','web/finale.css'])
    assert.equal(read(file),original(file),file+' unchanged from cinematic source');
const part=(s,start,end)=>s.slice(s.indexOf(start),s.indexOf(end));
const withoutAdminImports=s=>s.replace(/^.*(?:src="app-admin.js"|name="liceomap-api-base"|href="admin.css").*\n/gm,'');
assert.equal(part(withoutAdminImports(read('web/index.html')),'    <!-- Phase 4.5:','    <div id="admin-modal"'),
             part(original('web/index.html'),'    <!-- Phase 4.5:','    <div id="admin-modal"'),'Cinematic and presentation HTML preserved');
assert.equal(read('web/app.js').split('const adminModal')[0],original('web/app.js').split('const adminModal')[0],
    'Cinematic entry and navigation JS preserved');
console.log('PASS: cinematic source integrity, only authorized administration changed.');
