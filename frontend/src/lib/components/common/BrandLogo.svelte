<script>
  import logo from "$lib/assets/sadaqi-full-logo.svg";
</script>

<div class="brand-logo-wrap">
  <img src={logo} alt="Sadaqi logo" class="brand-logo" />
</div>

<style>
  .brand-logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 16px 0;
  }

  .brand-logo {
    width: min(520px, 88vw);
    height: auto;
    animation: logoFadeIn 0.8s ease both;
  }

  @keyframes logoFadeIn {
    from {
      opacity: 0;
      transform: translateY(-8px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
