<script>
  import { onMount } from 'svelte';
  import { api } from '$lib/api';
  let content = $state(null);
  let contentError = $state(false);
  onMount(async () => {
    try { content = await api('/content'); }
    catch { contentError = true; }
  });

  import ChatWidget from "$lib/components/chat/ChatWidget.svelte";
  import HeroSection from "$lib/components/sections/HeroSection.svelte";
  import AboutSection from "$lib/components/sections/AboutSection.svelte";
  import ProjectsSection from "$lib/components/sections/ProjectsSection.svelte";
  import ExperienceSection from "$lib/components/sections/ExperienceSection.svelte";
  import EducationSection from "$lib/components/sections/EducationSection.svelte";
  import ContactSection from "$lib/components/sections/ContactSection.svelte";
</script>
<main class="page">
  <HeroSection cv={content?.cv} />

  <div class="content">
    <AboutSection />
    <ProjectsSection />
    {#if content}
      <ExperienceSection experience={content.experience} />
    {:else}
      <section class="section"><h2>Arbeidserfaring</h2><p role="status">{contentError ? 'Arbeidserfaring kunne ikke hentes. Prøv å laste siden på nytt.' : 'Laster arbeidserfaring …'}</p></section>
    {/if}
    <EducationSection />
    <ContactSection />
  </div>

  <ChatWidget />
</main>

<style>
  .page {
    min-height: 100vh;
    background: #f8fafc;
  }

  .content {
    max-width: 1400px;
    margin: 0 auto;
    background: white;
  }

  :global(.section),
  :global(.about) {
    padding: 80px 40px;
  }

  :global(.section h2),
  :global(.about h2) {
    font-size: 36px;
    margin-bottom: 24px;
    color: #111827;
  }
</style>