<script>
  let { experience = [] } = $props();
</script>
<section id="experience" class="section experience">
  <h2>Arbeidserfaring</h2>
  <div class="timeline">
    {#each experience as entry}
      <article class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-content">
          <span class="timeline-date">{entry.period}</span>
          <h3>{entry.company}</h3>
          <p><strong>{entry.role}</strong>{entry.country ? ` · ${entry.country}` : ''}</p>
          <ul>{#each entry.tasks as task}<li>{task}</li>{/each}</ul>
        </div>
      </article>
    {/each}
  </div>
</section>

<style>
  .experience {
    background: white;
  }

  .timeline {
    position: relative;
    margin-top: 40px;
    padding-left: 40px;
  }

  .timeline::before {
    content: "";
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: #2563eb;
  }

  .timeline-item {
    position: relative;
    margin-bottom: 40px;
  }

  .timeline-dot {
    position: absolute;
    left: -38px;
    top: 8px;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #2563eb;
    border: 4px solid white;
    box-shadow: 0 0 0 2px #2563eb;
  }

  .timeline-content {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 24px;
    transition: all 0.2s ease;
  }

  .timeline-content:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  }

  .timeline-date {
    display: inline-block;
    margin-bottom: 10px;
    color: #2563eb;
    font-weight: 700;
  }

  .timeline-content h3 {
    margin: 0 0 12px;
    color: #111827;
  }

  .timeline-content p {
    margin: 0;
    line-height: 1.7;
    color: #4b5563;
  }
</style>
