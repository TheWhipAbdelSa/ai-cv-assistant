<script>
  let { openChat } = $props();
</script>

<button class="launcher-panel" onclick={openChat}>
  <div class="status-row">
    <span class="led"></span>
    <span class="status-text">ONLINE</span>
  </div>
  <div class="title">Abdel AI</div>
  <div class="subtitle">Information &</div>
  <div class="subtitle">Autmatisering</div>
</button>

<style>
  .launcher-panel {
    position: fixed;
    right: 0;
    top: 50%;
    transform: translateY(-50%);

    width: 170px;
    padding: 16px 18px;

    background: #111827;
    color: #f9fafb;

    border: 2px solid #22c55e;
    border-right: none;
    border-radius: 16px 0 0 16px;

    cursor: pointer;
    z-index: 999;

    text-align: left;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.35);

    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease;
  }

  .launcher-panel:hover {
    transform: translateY(-50%) translateX(-6px);
    transform: 0 20px 45px rgba(0, 0, 0, 0.45);
  }

  .status-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
  }

  .led {
    width: 10px;
    height: 10px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 12px #22c55e;
    animation: pulseLed 1.6s infinite;
  }

  .subtitle {
    font-size: 13px;
    color: #d1d5db;
    line-height: 1.35;
  }

  @keyframes pulseLed {
    0% {
      opacity: 0.45;
      transform: scale(0.9);
    }

    50% {
      opacity: 1;
      transform: scale(0.9);
    }

    100% {
      opacity: 0.45;
      transform: scale(0.9);
    }
  }
</style>
