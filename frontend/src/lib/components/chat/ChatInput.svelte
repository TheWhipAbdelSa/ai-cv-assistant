<script>
  let { inputMessage, setInputMessage, sendMessage, isLoading } = $props();

  $effect(() => {
    console.log("isLoading:", isLoading);
  });
</script>

<div class="chat-input">
  <input
    value={inputMessage}
    oninput={(event) => setInputMessage(event.target.value)}
    placeholder="Skriv spørsmålet ditt..."
    onkeydown={(event) => {
      if (event.key === "Enter" && !isLoading && inputMessage.trim()) {
        sendMessage();
      }
    }}
  />

  <button onclick={sendMessage} disabled={!inputMessage.trim() || isLoading}>
    {isLoading ? "Sender..." : "Send"}
  </button>
</div>

<style>
  .chat-input {
    display: flex;
    gap: 8px;
    padding: 14px;
    border-top: 1px solid #e5e7eb;
    background: white;
  }

  .chat-input input {
    flex: 1;
    padding: 12px;
    border: 1px solid #d1d5db;
    border-radius: 10px;
    font-size: 14px;
  }

  .chat-input button {
    min-width: 90px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    cursor: pointer;
  }

  .chat-input button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
