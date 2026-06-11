<script>
  let { messages, isTyping } = $props();
</script>

<div class="chat-messages">
  {#each messages as message}
    <div
      class="message"
      class:bot={message.from === "bot"}
      class:user={message.from === "user"}
    >
      {message.text}
      <div class="message-time">{message.time}</div>
    </div>
  {/each}

  {#if isTyping}
    <div class="message bot typing">
      <span></span>
      <span></span>
      <span></span>
    </div>
  {/if}
</div>

<style>
  .chat-messages {
    flex: 1;
    padding: 18px;
    background: #f9fafb;
    overflow-y: auto;
  }

  .message {
    max-width: 80%;
    padding: 12px 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    font-size: 14px;
    line-height: 1.4;
  }

  .bot {
    background: #e5e7eb;
    color: #111827;
  }

  .user {
    background: #2563eb;
    color: white;
    margin-left: auto;
  }

  .message-time {
    font-size: 11px;
    margin-top: 5px;
    opacity: 0.6;
  }

  .user .message-time {
    color: white;
  }

  .typing {
    display: flex;
    gap: 5px;
    align-items: center;
    width: fit-content;
  }

  .typing span {
    width: 7px;
    height: 7px;
    background: #6b7280;
    border-radius: 50%;
    animation: blink 1.4s infinite;
  }

  .typing span:nth-child(2) {
    animation-delay: 0.2s;
  }

  .typing span:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes blink {
    0%,
    100% {
      opacity: 0.2;
    }

    50% {
      opacity: 1;
    }
  }
</style>
