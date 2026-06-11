<script>
  import ChatLauncher from "./ChatLauncher.svelte";
  import ChatWindow from "./ChatWindow.svelte";
  
  let isChatOpen = $state(false);
  function openChat() {
    isChatOpen = true;
  }

  function closeChat() {
    isChatOpen = false;
  }

  
</script>

{#if !isChatOpen}
  <ChatLauncher {openChat} />
{/if}

{#if isChatOpen}
  <ChatWindow {closeChat} />
{/if}

