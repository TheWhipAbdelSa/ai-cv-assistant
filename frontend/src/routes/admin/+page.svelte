<script>
  import { api, apiBase } from '$lib/api';
  let token = $state('');
  let authenticated = $state(false);
  let busy = $state(false);
  let error = $state('');
  let notice = $state('');
  let entries = $state([]);
  let cv = $state(null);
  let selectedFile = $state(null);
  let fileInput = $state(null);
  const headers = () => ({ Authorization: `Bearer ${token}` });

  async function run(action) {
    busy = true; error = ''; notice = '';
    try { await action(); }
    catch (e) { error = e.message || 'Noe gikk galt. Prøv igjen.'; }
    finally { busy = false; }
  }
  function login(event) {
    event.preventDefault();
    run(async () => {
      const data = await api('/admin/content', { headers: headers() });
      entries = data.experience.map(entry => ({ ...entry, taskText: entry.tasks.join('\n') }));
      cv = data.cv;
      authenticated = true;
    });
  }
  function save(event) {
    event.preventDefault();
    run(async () => {
      const experience = entries.map(({ taskText, ...entry }) => ({
        ...entry, tasks: taskText.split('\n').map(t => t.trim()).filter(Boolean)
      }));
      await api('/admin/experience', {
        method: 'PUT', headers: { ...headers(), 'Content-Type': 'application/json' },
        body: JSON.stringify({ experience })
      });
      notice = 'Arbeidserfaringen er publisert på nettsiden og oppdatert for AI-assistenten.';
    });
  }
  function upload(event) {
    event.preventDefault();
    run(async () => {
      if (!selectedFile) throw new Error('Velg en PDF-fil først.');
      if (selectedFile.size > 10 * 1024 * 1024) throw new Error('Filen kan være maks 10 MB.');
      const body = new FormData(); body.append('file', selectedFile);
      const data = await api('/admin/cv', { method: 'POST', headers: headers(), body });
      cv = data.cv; selectedFile = null; fileInput.value = '';
      notice = 'Den nye CV-en er publisert og tilgjengelig for nedlasting.';
    });
  }
  function logout() {
    authenticated = false; token = ''; entries = []; selectedFile = null; error = ''; notice = '';
  }
</script>

<svelte:head>
  <title>Kontrollpanel · Abdel Sadaqi</title>
  <meta name="robots" content="noindex, nofollow" />
</svelte:head>

<main>
  <header>
    <div><a href="/">← Til nettsiden</a><h1>Kontrollpanel</h1><p>Hold CV og arbeidserfaring oppdatert.</p></div>
    {#if authenticated}<button class="secondary" onclick={logout} disabled={busy}>Logg ut</button>{/if}
  </header>
  {#if error}<p class="error" role="alert">{error}</p>{/if}
  {#if notice}<p class="success" role="status">{notice}</p>{/if}

  {#if !authenticated}
    <section class="login">
      <h2>Logg inn</h2>
      <p>Bruk administratornøkkelen som er konfigurert på serveren.</p>
      <form onsubmit={login}>
        <label for="key">Administratornøkkel</label>
        <input id="key" type="password" bind:value={token} autocomplete="current-password" required />
        <button disabled={busy}>{busy ? 'Logger inn …' : 'Logg inn'}</button>
      </form>
    </section>
  {:else}
    <section>
      <h2>CV-dokument</h2>
      <p>Last opp en PDF på opptil 10 MB. Den erstatter CV-en som besøkende kan laste ned.</p>
      <a href={cv ? `${apiBase}/cv` : '/Abdel-Sadaqi-CV.pdf'} target="_blank" rel="noreferrer">Se gjeldende CV ↗</a>
      {#if cv}<p class="muted">Oppdatert {new Date(cv.updated_at).toLocaleDateString('nb-NO')}</p>{/if}
      <form onsubmit={upload}>
        <fieldset disabled={busy}>
          <label for="cv">Ny CV (PDF)</label>
          <input bind:this={fileInput} id="cv" type="file" accept=".pdf,application/pdf" required onchange={event => selectedFile = event.currentTarget.files?.[0] || null} />
          <p class="muted">PDF-teksten importeres ikke til AI-assistenten. Oppdater arbeidserfaringen under separat.</p>
          <button>{busy ? 'Vent …' : 'Last opp og publiser CV'}</button>
        </fieldset>
      </form>
    </section>
    <section>
      <h2>Arbeidserfaring</h2>
      <p>Endringene blir synlige på nettsiden og brukes i nye AI-svar når du publiserer. Legg nyeste erfaring øverst.</p>
      <form onsubmit={save}>
        <fieldset disabled={busy}>
          {#each entries as entry, index}
            <article>
              <div class="row"><h3>{entry.company || 'Ny arbeidserfaring'}</h3><button type="button" class="danger" onclick={() => entries = entries.filter((_, i) => i !== index)}>Fjern</button></div>
              <div class="grid">
                <label>Arbeidsgiver<input bind:value={entry.company} required maxlength="200" /></label>
                <label>Stilling<input bind:value={entry.role} required maxlength="200" /></label>
                <label>Periode<input bind:value={entry.period} placeholder="Januar 2026 – nå" required maxlength="100" /></label>
                <label>Land<input bind:value={entry.country} maxlength="100" /></label>
              </div>
              <label>Arbeidsoppgaver – én per linje<textarea bind:value={entry.taskText} rows="4" maxlength="60000"></textarea></label>
              <div class="row">
                <button type="button" class="secondary" disabled={index === 0} onclick={() => { [entries[index - 1], entries[index]] = [entries[index], entries[index - 1]]; }}>Flytt opp</button>
                <button type="button" class="secondary" disabled={index === entries.length - 1} onclick={() => { [entries[index + 1], entries[index]] = [entries[index], entries[index + 1]]; }}>Flytt ned</button>
              </div>
            </article>
          {:else}<p>Ingen arbeidserfaring lagt til.</p>{/each}
          <div class="row actions">
            <button type="button" class="secondary" onclick={() => entries = [{ company: '', role: '', period: '', country: '', tasks: [], taskText: '' }, ...entries]}>+ Legg til arbeidserfaring</button>
            <button>{busy ? 'Vent …' : 'Publiser arbeidserfaring'}</button>
          </div>
        </fieldset>
      </form>
    </section>
  {/if}
</main>

<style>
  :global(body) { margin: 0; background: #f8fafc; font-family: system-ui, sans-serif; color: #172033; }
  main { max-width: 960px; margin: auto; padding: 40px 24px 80px; }
  header, .row { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
  h1 { font-size: 36px; margin-bottom: 8px; } h2 { margin-top: 0; } h3 { margin: 0; }
  p { line-height: 1.6; } a { color: #2563eb; } .muted { color: #64748b; font-size: 14px; }
  section { background: white; border: 1px solid #dbe3ef; border-radius: 20px; padding: 28px; margin-top: 24px; }
  .login { max-width: 440px; } fieldset { border: 0; padding: 0; margin: 0; min-width: 0; }
  label { display: block; font-weight: 600; margin: 16px 0 8px; }
  input, textarea { display: block; box-sizing: border-box; width: 100%; padding: 12px; margin: 8px 0 16px; border: 1px solid #b7c3d4; border-radius: 8px; font: inherit; }
  textarea { resize: vertical; } button { border: 0; background: #2563eb; color: white; padding: 12px 18px; border-radius: 10px; font: inherit; font-weight: 600; cursor: pointer; }
  button:disabled { opacity: .5; cursor: default; } .secondary { background: #eaf0fb; color: #214b93; } .danger { background: #fff0f0; color: #b42318; }
  article { margin: 24px 0; padding: 24px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 20px; }
  .error, .success { padding: 16px; border-radius: 10px; } .error { background: #fee2e2; color: #991b1b; } .success { background: #dcfce7; color: #166534; }
  @media(max-width: 600px) { .grid { grid-template-columns: 1fr; } main { padding: 24px 16px; } section, article { padding: 18px; } }
</style>
