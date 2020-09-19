/**
 * Add a new tweet text area
 */
function addTweet() {
    // Create the text area
    const tweetTextarea = document.createElement("textarea");
    tweetTextarea.classList.add("border-2", "rounded", "block", "w-full", "h-32", "my-1");
    // Add handler for input changes
    tweetTextarea.addEventListener("input", (event) => {
        const tweetSizeSpan = event.target.parentNode.getElementsByTagName("span")[0];
        const tweetSize = event.target.value.length;

        // Change the color of the tweet size counter
        tweetSizeSpan.classList.remove("text-black", "text-orange-500", "text-red-700");
        if (tweetSize <= 250) tweetSizeSpan.classList.add("text-black");
        else if (tweetSize <= 280) tweetSizeSpan.classList.add("text-orange-500");
        else tweetSizeSpan.classList.add("text-red-700");

        // Change the text of the tweet size counter
        tweetSizeSpan.innerHTML = tweetSize + " / 280";
    });

    // Create the tweet size counter
    const tweetSizeCounter = document.createElement("span");
    tweetSizeCounter.classList.add("text-xl", "text-right");
    tweetSizeCounter.innerHTML = "0 / 280";

    // Create the remove button
    const tweetRemoveButton = document.createElement("button");
    tweetRemoveButton.classList.add("ml-10", "text-blue-500", "hover:text-blue-700");
    tweetRemoveButton.innerHTML = "✕";
    tweetRemoveButton.addEventListener("click", (event) => {
        event.target.parentNode.remove();
    });

    // Create a div to hold all elements together
    const tweetDiv = document.createElement("div");
    tweetDiv.classList.add("w-full", "lg:w-1/2", "mx-auto", "text-right", "my-6");
    tweetDiv.appendChild(tweetSizeCounter);
    tweetDiv.appendChild(tweetRemoveButton);
    tweetDiv.appendChild(tweetTextarea);

    // Add the div to the page
    document.getElementById("text-container").appendChild(tweetDiv);

    // Focus on the new text area
    tweetTextarea.focus();
}

/**
 * Initiate a file download
 * @param {*} filename name of the file
 * @param {*} content content of the file
 */
function downloadFile(filename, content) {
    // Copied from https://ourcodeworld.com/articles/read/189/how-to-create-a-file-and-generate-a-download-with-javascript-in-the-browser-without-a-server
    const element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(content));
    element.setAttribute("download", filename);

    element.style.display = "none";
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

/**
 * Create a yaml file from the tweets and initiate a download
 */
function downloadThreadAsYaml() {
    // Create header
    let yamlContent = "thread:\n";
    yamlContent += "  target: \n";
    yamlContent += "  tweets:\n";
    const tweets = document.getElementsByTagName("textarea");

    // Populate all tweets
    [...tweets].forEach((tweet) => {
        const tweetContent = tweet.value.replaceAll("\n", "\n        ");
        yamlContent += "    - text: |\n        ";
        yamlContent += tweetContent + "\n";
    });

    // Initiate a download
    downloadFile("thread.yaml", yamlContent);
}

/**
 * Initialize all actions
 */
function init() {
    // Add the first tweet text area
    addTweet();

    // Donload thread button
    document.getElementById("download-thread-button").addEventListener("click", (event) => {
        downloadThreadAsYaml();
    });

    // Add new tweet button
    document.getElementById("new-tweet-button").addEventListener("click", (event) => {
        addTweet();
    });
}

if (document.readyState !== "loading") {
    init();
} else {
    document.addEventListener("DOMContentLoaded", init);
}
