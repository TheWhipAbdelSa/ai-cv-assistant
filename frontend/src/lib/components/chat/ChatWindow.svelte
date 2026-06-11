<script>
  import { fly } from "svelte/transition";
  import { tick } from "svelte";

  import ChatHeader from "./ChatHeader.svelte";
  import ChatInput from "./ChatInput.svelte";
  import ChatMessages from "./ChatMessages.svelte";
  import { dev } from "$app/env";

  let { closeChat } = $props();

  let inputMessage = $state("");
  let isLoading = $state(false);
  let isTyping = $state(false);
  let chatMessagesContainer = $state(null);

  function getTime() {
    const now = new Date();
    return now.toLocaleTimeString("no-NO").slice(0, 5);
  }

  let messages = $state([
    {
      from: "bot",
      text: "Hei, Jeg er Abdels AI-Assistent.",
      time: getTime(),
    },
  ]);
  async function scrollToBottom() {
    await tick();

    if (chatMessagesContainer) {
      chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
    }
  }
  // #region en asynkron funksjon for å sende chat-melding.

  async function sendMessage() {
    if (!inputMessage.trim() || isLoading) return;

    const userText = inputMessage.trim();

    messages = [
      ...messages,
      {
        from: "user",
        text: userText,
        time: getTime(),
      },
    ];

    inputMessage = "";
    isLoading = true;
    isTyping = true;

    await scrollToBottom();

    try {
      console.log("API URL:", import.meta.env.VITE_API_URL);
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userText }),
      });

      const data = await response.json();

      await typeMessage(
        data.answer ?? "Jeg fikk ikke et gyldig svar fra serveren.",
      );
    } catch (error) {
      messages = [
        ...messages,
        {
          from: "bot",
          text: "Kunne ikke kontakte serveren.",
          time: getTime(),
        },
      ];
    } finally {
      isTyping = false;
      isLoading = false;
      await scrollToBottom();
    }
  }
  async function typeMessage(fullText) {
    let displayedText = "";

    messages = [
      ...messages,
      {
        from: "bot",
        text: "",
        time: getTime(),
      },
    ];

    const messageIndex = messages.length - 1;

    for (let i = 0; i < fullText.length; i++) {
      displayedText += fullText[i];

      messages[messageIndex].text = displayedText;
      messages = [...messages];

      await scrollToBottom();
      await new Promise((resolve) => setTimeout(resolve, 15));
    }
  }
  // #endregion
</script>

<div class="chat-popup" in:fly={{ x: 400, duration: 250 }}>
  <ChatHeader {closeChat} />

  <div class="chat-messages" bind:this={chatMessagesContainer}>
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

  <ChatInput
    {inputMessage}
    setInputMessage={(value) => (inputMessage = value)}
    {sendMessage}
    {isLoading}
  />
</div>

<style>
  .chat-popup {
    position: fixed;
    right: 30px;
    bottom: 95px;
    width: 420px;
    height: 600px;
    background: white;
    border-radius: 18px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 9999;
  }

  @media (max-width: 768px) {
    .chat-popup {
      width: 100vw;
      height: 100vh;
      right: 0;
      bottom: 0;
      border-radius: 0;
    }
  }

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
</style>
