const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");


// Add message to chat
function addMessage(text, type) {

    const message = document.createElement("div");
    message.className = "message " + type;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = type === "user" ? "👩" : "🤖";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    message.appendChild(avatar);
    message.appendChild(bubble);

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// Send message to Python Flask backend
async function sendToBackend(message) {

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        if (!response.ok) {
            throw new Error("Server error");
        }


        const data = await response.json();


        addMessage(
            data.reply,
            "bot"
        );

    }

    catch (error) {

        console.error(error);

        addMessage(
            "Sorry! I couldn't connect to the chatbot server. 😕",
            "bot"
        );

    }

}


// Send normal typed message
function sendMessage(event) {

    event.preventDefault();

    const text = userInput.value.trim();


    if (text === "") {
        return;
    }


    // Show user message
    addMessage(
        text,
        "user"
    );


    // Clear input
    userInput.value = "";


    // Send to Python
    sendToBackend(text);

}


// Quick question buttons
function quickQuestion(question) {

    // Show user's question
    addMessage(
        question,
        "user"
    );


    // Send question to Python
    sendToBackend(question);

}