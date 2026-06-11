<script>
  let { closeChat } = $props();
</script>

<div class="chat-header">
  <div class="assistant-info">
    <div class="avatar">A</div>

    <div>
      <div class="status-row">
        <span class="led"></span>
        <span class="status-text">ONLINE</span>
      </div>

      <strong>Abdel AI</strong>
      <span class="subtitle">Informatikk & Automatisering</span>
    </div>
  </div>

  <button class="close-button" onclick={closeChat}>x</button>
</div>

<style>
  .chat-header {
    background: #111827;
    color: white;
    padding: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .assistant-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
  }

  .status-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 3px;
  }

  .led {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 10px #22c55e;
  }

  .status-text {
    font-size: 11px;
    letter-spacing: 1.4px;
    color: #86efac;
    font-weight: 700;
  }

  .subtitle {
    display: block;
    font-size: 12px;
    color: #9ca3af;
    margin-top: 3px;
  }

  .close-button {
    background: transparent;
    color: white;
    border: none;
    font-size: 28px;
    cursor: pointer;
  }
</style>
