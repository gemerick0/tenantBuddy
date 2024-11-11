<script>
    import Message from '$lib/Message.svelte';
    import { writable } from 'svelte/store';
    import logo from '$lib/assets/logo.png?enhanced';
    import send from '$lib/assets/send.png?enhanced';
    import mic from '$lib/assets/mic.png?enhanced';
    import {
	blur,
	crossfade,
	draw,
	fade,
	fly,
	scale,
	slide
} from 'svelte/transition';

    let pressed = writable(false);

    let text = writable('');
    let element;

    let messages = $state([
    ]);

    const send_message = async (text) => {
		let res;
		try {
            messages.push({message: `${text}`, sender: 'user'});
			res = await fetch(`http://127.0.0.1:8000/messages/?q=${text}`);
            const data = await res.json();
            await messages.push({ message: `${data.message}`, sender: 'bot' });
        }
        catch (error) {
            console.error('Error:', error);
        }
        scrollToBottom(element);
	};

    const scrollToBottom = async (node) => {
        node.scroll({ top: node.scrollHeight, behavior: 'smooth' });
    }; 

</script>

<style>
    .logo {
        width: 130px; /* Adjust the size as needed */
        height: auto;
        display: block;
        margin-left: 0; /* Align to the left */
    }
    .send {
        width: 40px; /* Adjust the size as needed */
        height: auto;
        display: block;
        margin-left: 0; /* Align to the left */
    }
    .mic {
        width: 20px; /* Adjust the size as needed */
        height: auto;
        display: block;
        margin-left: 0; /* Align to the left */
    }
</style>

<div class="self-center bg-white pl-28 pt-6 pb-7">
<div class="mockup-phone border-primary">
    <div class="camera"></div>
    <div class="display">
      <div class="artboard artboard-demo phone-1 bg-white">



        <div class=" header flex mb-auto self-start h-[90px] w-full bg-bluely items-center content-center p-5 pt-10">
            <div> 
            <enhanced:img class = "logo mt-2" alt="The project logo" src={logo}/>
            </div>
            <button onclick={() => pressed.set(true)} class="btn btn-ghost bg-greyiaa text-gray-400 ml-auto">Share</button>  
        </div>

        {#if $pressed}
        <div in:blur class="absolute z-50">
            <div class="card glass w-40 shadow-xl shadow-gray-400">
                <div class="card-body items-center text-center">
                  <h2 class="card-title">Generating</h2>
                  <span class="loading loading-ball loading-lg"></span>
                </div>
              </div>
        </div>
        {/if}
        
        <div bind:this={element} class="chat-container overflow-auto scroll-smooth [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none] ">
            <div class="chat chat-start m-1 ml-2">
                <div class="chat-bubble bg-greyiaa shadow-md shadow-stone-300 text-black rounded-3xl">
                    Great to meet you, my name is Tendant Buddy. What is the issue in your home?
                </div>
            </div>
            {#each messages as message}
            <Message chat_message={message} />
            {/each}
        </div>
        

        <form
        onsubmit={() => {
            send_message($text);
            $text = '';
        }}
        >
        <div class="flex-auto flex h-30 gap-2 mr-5 px-5 pt-2 border-t-2 w-full">
        <input bind:value = {$text} type="text" placeholder="Message" class="left-2 relative input w-full max-w-xs mt-auto mb-[7px] pr-12 rounded-full border-neutral-300 border-2 bg-white grid" />
        <button type="submit" class="mt-0 mb-2 relative -left-8" aria-label="Submit">
            <enhanced:img class = "mic " alt="mic" src={mic}/>
        </button>
        <button type="submit" class="mt-0 mb-2 relative -left-2 " aria-label="Submit">
            <enhanced:img class = "send " alt="send" src={send}/>
        </button>
        </div>
    </form>

      </div>
    </div>
  </div>
       




</div>