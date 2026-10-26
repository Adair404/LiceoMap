/* Tokens exist only in this closure; one controller owns real administration. */
(() => {
    'use strict';
    const $ = id => document.getElementById(id);
    const base = new URL(document.querySelector('meta[name="liceomap-api-base"]').content);
    if (base.protocol !== 'https:' && !(base.protocol === 'http:' && ['localhost','127.0.0.1'].includes(base.hostname))) throw Error('La API requiere HTTPS o un destino local.');
    const roles = ['dev','utp','inspectoria'];
    let token = null, user = null, timer, editing = null, epoch = 0, listVersion = 0;
    let controller = new AbortController();
    localStorage.removeItem('liceomap_session');
    function resetForm() {
        editing = null; $('announcement-form').reset();
        $('announcement-save').textContent = 'Publicar anuncio';
        $('announcement-cancel').hidden = true; $('announcement-status').textContent = '';
    }
    function clearSession(message = '') {
        localStorage.removeItem('liceomap_session');
        epoch++; listVersion++; controller.abort(); controller = new AbortController();
        token = null; user = null; clearTimeout(timer); resetForm();
        $('announcement-list').replaceChildren(); $('announcement-list-status').textContent = '';
        $('admin-user-name').textContent = ''; $('admin-login-status').textContent = message;
        window.dispatchEvent(new Event('liceomap:session-ended'));
    }
    async function request(path, options = {}) {
        const session = epoch;
        let response;
        try {
            response = await fetch(new URL(path, base), {...options,
                signal:AbortSignal.any([controller.signal, AbortSignal.timeout(12000)]),
                cache:'no-store', credentials:'omit', redirect:'error',
                headers:{'Content-Type':'application/json', ...(token ? {Authorization:`Bearer ${token}`} : {})}});
        } catch (_) {
            throw Error(session !== epoch ? 'Operación cancelada.' : 'No se pudo conectar con el servidor. Revisa la conexión y vuelve a intentar.');
        }
        if (session !== epoch) throw Error('Operación cancelada.');
        const data = response.status === 204 ? null : await response.json().catch(() => null);
        if (!response.ok) {
            if (response.status === 401 && token) clearSession('La sesión expiró. Inicia sesión nuevamente.');
            if (response.status === 403 && token) clearSession('Ya no tienes permiso para administrar.');
            throw Error(typeof data?.detail === 'string' ? data.detail : 'No se pudo completar la operación.');
        }
        return data;
    }
    async function login(rut, password) {
        clearSession();
        const data = await request('auth/login', {method:'POST',body:JSON.stringify({rut,password})});
        token = data.access_token;
        try {
            user = await request('me');
            if (!roles.includes(user.rol)) {
                await request('auth/logout', {method:'POST'});
                throw Error('Tu rol no tiene acceso al panel administrativo.');
            }
            timer = setTimeout(() => clearSession('La sesión expiró. Inicia sesión nuevamente.'), data.expires_in * 1000);
            return user;
        } catch (error) { clearSession(); throw error; }
    }
    function logout() {
        const oldToken = token; clearSession();
        if (oldToken) fetch(new URL('auth/logout',base), {method:'POST',
            headers:{Authorization:`Bearer ${oldToken}`}, credentials:'omit', redirect:'error',
            signal:AbortSignal.timeout(5000), keepalive:true}).catch(() => {});
    }
    const text = (tag,value) => { const node = document.createElement(tag); node.textContent = value; return node; };
    async function loadList() {
        const version = ++listVersion;
        const params = new URLSearchParams({estado:$('announcement-state').value});
        if ($('announcement-recipient').value) params.set('destinatario',$('announcement-recipient').value);
        $('announcement-list-status').textContent = 'Cargando anuncios…';
        try {
            const items = await request('admin/anuncios?' + params);
            if (version !== listVersion || !user) return;
            $('announcement-list').replaceChildren(...items.map(item => {
                const card = document.createElement('article'); card.className = 'announcement-item';
                card.dataset.announcementId = item.id_anuncio;
                card.append(text('h4',item.titulo),text('p',item.contenido),
                    text('p',`${item.publicado ? 'Publicado' : 'Retirado'} · ${item.id_curso || 'Toda la comunidad'} · ${item.prioridad}`),
                    text('small',`${item.autor} · ${new Date(item.fecha_publicacion).toLocaleString('es-CL',{timeZone:'America/Santiago'})}`));
                if (item.publicado) {
                    const actions = document.createElement('div'); actions.className = 'announcement-actions';
                    const edit = text('button','Editar'), withdraw = text('button','Retirar');
                    for (const button of [edit,withdraw]) { button.type = 'button'; button.className = 'btn-dash-secondary'; }
                    edit.addEventListener('click', () => {
                        editing = item.id_anuncio;
                        $('demo-announcement-title').value = item.titulo; $('demo-announcement-body').value = item.contenido;
                        $('demo-announcement-level').value = item.prioridad; $('announcement-course').value = item.id_curso || '';
                        $('announcement-save').textContent = 'Guardar cambios'; $('announcement-cancel').hidden = false;
                        $('demo-announcement-title').focus();
                    });
                    withdraw.addEventListener('click', async () => {
                        if (!confirm('¿Retirar este anuncio? Se conservará su historial.')) return;
                        withdraw.disabled = true;
                        try {
                            await request(`anuncios/${item.id_anuncio}`,{method:'DELETE'});
                            if (editing === item.id_anuncio) resetForm();
                            $('announcement-status').textContent = 'Anuncio retirado.'; await loadList();
                        } catch (error) { $('announcement-status').textContent = error.message;
                        } finally { withdraw.disabled = false; }
                    });
                    actions.append(edit,withdraw); card.append(actions);
                }
                return card;
            }));
            $('announcement-list-status').textContent = `${items.length} anuncio(s).`;
        } catch (error) {
            if (version === listVersion) $('announcement-list-status').textContent = error.message;
            throw error;
        }
    }
    async function refresh() {
        const courses = await request('admin/cursos');
        for (const [id,first] of [['announcement-course','Toda la comunidad'],['announcement-recipient','Todos']]) {
            const select = $(id), previous = select.value;
            select.replaceChildren(new Option(first,''));
            if (id === 'announcement-recipient') select.add(new Option('Toda la comunidad','global'));
            courses.forEach(course => select.add(new Option(course.nombre,course.id_curso)));
            select.value = previous;
        }
        await loadList();
    }
    $('announcement-form').addEventListener('submit', async event => {
        event.preventDefault();
        if (!token || !roles.includes(user?.rol)) return;
        const save = $('announcement-save'), aid = editing;
        const payload = {titulo:$('demo-announcement-title').value.trim(),contenido:$('demo-announcement-body').value.trim(),
            prioridad:$('demo-announcement-level').value,id_curso:$('announcement-course').value || null};
        save.disabled = true; $('announcement-status').textContent = 'Guardando…';
        try {
            await request(aid ? `anuncios/${aid}` : 'anuncios',{method:aid ? 'PATCH':'POST',body:JSON.stringify(payload)});
            resetForm(); $('announcement-status').textContent = aid ? 'Cambios guardados.' : 'Anuncio publicado.';
            await loadList();
        } catch (error) { $('announcement-status').textContent = error.message;
        } finally { save.disabled = false; }
    });
    $('announcement-cancel').addEventListener('click',resetForm);
    ['announcement-state','announcement-recipient'].forEach(id => $(id).addEventListener('change',() => loadList().catch(() => {})));
    $('announcement-refresh').addEventListener('click',() => refresh().catch(error => { $('announcement-list-status').textContent = error.message; }));
    ['horarios','salas','usuarios'].forEach(name => {
        const button = $(`tab-button-${name}`); button.disabled = true; button.title = 'En desarrollo';
        button.append(document.createTextNode(' · En desarrollo'));
        $(`tab-${name}`).replaceChildren(text('p','En desarrollo.'));
    });
    Object.defineProperty(window,'LiceoMapAdmin',{value:Object.freeze({
        get authorized() { return !!token && roles.includes(user?.rol); },
        login,logout,refresh,cancelLogin() { if (!user) clearSession(); }
    })});
})();
