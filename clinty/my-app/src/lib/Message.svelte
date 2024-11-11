<script>
    let { chat_message } = $props();
    
</script>

{#if chat_message.sender == 'user'}
<div class="chat chat-end m-1 mr-2">
    <div value = {chat_message} class="chat-bubble  bg-bluely shadow-md shadow-stone-300 text-white rounded-3xl">
        {chat_message.message}
    </div>
</div>
{:else}
<div class="chat chat-start m-1 ml-2 ">
    <div value = {chat_message} class="chat-bubble  bg-greyiaa shadow-md shadow-stone-300 text-black rounded-3xl">
        {chat_message.message}
    </div>
</div>
{/if}

