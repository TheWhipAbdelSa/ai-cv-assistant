<section id="projects" class="section">
  <h2>Prosjekter</h2>

  <div class="project-grid">
    <article class="project-card">
      <div class="project-icon">🤖</div>
      <h3>AI-basert CV-assistent</h3>

      <p>
        Personlig AI-assistent som svarer på spørsmål om utdanning, erfaring,
        prosjekter og ferdigheter basert på strukturert profil-data.
      </p>

      <div class="project-tags">
        <span>SvelteKit</span>
        <span>FastAPI</span>
        <span>OpenAI</span>
        <span>Python</span>
      </div>

      <a
        href="https://github.com/TheWhipAbdelSa/ai-cv-assistant"
        target="_blank"
        rel="noopener noreferrer"
      >
        Se på GitHub
      </a>
    </article>

    <article class="project-card">
      <div class="project-icon">⚙️</div>
      <h3>Automatisering og PLS</h3>

      <p>
        Praktisk læring og prosjekter innen TIA Portal, CODESYS, SCADA-systemer,
        styring, sensorer og industriell automasjon.
      </p>

      <div class="project-tags">
        <span>TIA Portal</span>
        <span>CODESYS</span>
        <span>SCADA</span>
        <span>PLS</span>
      </div>
    </article>

    <article class="project-card">
      <div class="project-icon">🖨️</div>
      <h3>Embedded og 3D-printing</h3>

      <p>
        Hobby- og læringsprosjekter med ESP32, Arduino, sensorer, motorstyring,
        servoer, CAD-design og 3D-printing.
      </p>

      <div class="project-tags">
        <span>ESP32</span>
        <span>Arduino</span>
        <span>FreeCAD</span>
        <span>3D-printing</span>
      </div>
    </article>
  </div>
</section>

<style>
  .project-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }

  .project-card {
    padding: 28px;
    border-radius: 22px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    transition: all 0.2s ease;
  }

  .project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
  }

  .project-icon {
    font-size: 34px;
    margin-bottom: 16px;
  }

  .project-card h3 {
    margin: 0 0 14px;
    color: #111827;
  }

  .project-card p {
    color: #4b5563;
    line-height: 1.7;
  }

  .project-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 18px 0;
  }

  .project-tags span {
    padding: 7px 12px;
    border-radius: 999px;
    background: white;
    border: 1px solid #d1d5db;
    font-size: 13px;
  }

  .project-card a {
    display: inline-flex;
    margin-top: 8px;
    color: #2563eb;
    font-weight: 700;
    text-decoration: none;
  }

  .project-card a:hover {
    text-decoration: underline;
  }

  @media (max-width: 800px) {
    .project-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
