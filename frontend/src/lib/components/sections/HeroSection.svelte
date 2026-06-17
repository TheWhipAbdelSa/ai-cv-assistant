<script>
  import backgroundImage from "$lib/images/background.jpeg";
  import CvCard from "$lib/components/common/CvCard.svelte";
  import BrandLogo from "$lib/components/common/BrandLogo.svelte";
</script>

<main>
  <BrandLogo />
  <section class="hero">
    <div class="hero-content">
      <h1>Abdel Sadaqi</h1>

      <p class="description">
        Nyutdannet elektroingeniør med bachelor i informatikk og automatisering.
        Jeg har interesse for PLS-programmering, SCADA, industrielle
        kontrollsystemer og softwareutvikling. Utforsk prosjektene mine eller
        spør AI-assistenten om min erfaring og kompetanse.
      </p>

      <div class="actions">
        <a href="#projects">Se prosjekter</a>

        <a href="#contact" class="secondary">Kontakt</a>
      </div>

      <div class="skills">
        <span>Siemens TIA Portal</span>
        <span>PLC</span>
        <span>SCADA</span>
        <span>Ignition</span>
        <span>Python</span>

        <span>ESP32 / IoT</span>
        <span>SvelteKit</span>
        <span>FastAPI</span>
        <span>OpenAI</span>

        <span>SQL</span>
        <span>C#</span>
      </div>
      <CvCard />
    </div>
    <div class="hero-image">
      <img src={backgroundImage} alt="Abdel Sadaqi" />
    </div>
  </section>
</main>

<style>
  main {
    padding-top: 40px;
  }
  .hero {
    min-height: calc(100vh - 220px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 60px;
    padding: 40px;
  }

  .hero-content {
    flex: 1;
    max-width: 700px;
  }

  .hero-image {
    flex: 1;
    display: flex;
    justify-content: center;
  }

  .hero-image img {
    width: 100%;
    max-width: 600px;
    border-radius: 20px;
    object-fit: cover;
  }

  h1 {
    font-size: 64px;
    margin: 0 0 18px;
    color: #111827;
  }

  .description {
    font-size: 22px;
    line-height: 1.6;
    color: #374151;
    margin-bottom: 30px;
  }

  .actions {
    display: flex;
    gap: 14px;
  }

  .actions a {
    padding: 13px 22px;
    border-radius: 999px;
    background: #2563eb;
    color: white;
    text-decoration: none;
    font-weight: 700;
  }

  .actions .secondary {
    background: white;
    color: #2563eb;
    border: 1px solid #2563eb;
  }

  @media (max-width: 700px) {
    .hero {
      padding: 24px;
      align-items: flex-start;
      padding-top: 100px;
    }

    h1 {
      font-size: 42px;
    }

    .description {
      font-size: 18px;
    }

    .actions {
      flex-direction: column;
      align-items: flex-start;
    }
  }

  .skills {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 25px 0;
  }

  .skills span {
    padding: 8px 14px;
    background: white;
    border-radius: 999px;
    border: 1px solid #d1d5db;
    font-size: 14px;
  }
</style>
