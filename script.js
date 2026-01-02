// script.js

const daysCounterElement = document.getElementById('days-counter');
const timeSince = calculateDaysSince("2026-01-01");
daysCounterElement.innerText = `Day ${timeSince}`;
fetchQuote(timeSince);

/* calculateDaysSince(date) computes the number of days (floor)
   since a given start date.
*/
function calculateDaysSince(date) {
    const now = new Date();
    const startDate = new Date(date);
    const difference = now - startDate;
    return Math.floor(difference / (1000 * 60 * 60 * 24)); 
}

/* fetchQuote(timeSince) is called on load of the page.
   It fetches the JSON list of Steinbeck quotes, selects
   one quote according to the given date index, and initializes
   the animations.
*/
async function fetchQuote(timeSince) {
    try {
        const [response1] = await Promise.all([
            fetch('static/all_quotes_filtered.json')
        ]);
        const quoteList = await response1.json();

        const index = timeSince % quoteList.length;

        const quoteElement = document.getElementById('quote');
        quoteElement.innerText = quoteList[index]['quote'];
        const sourceElement = document.getElementById('source');
        sourceElement.innerText = quoteList[index]['book'];

        chooseFont(quoteElement);
        runAnimations();

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

/* chooseFont(element) assigns a random font to the
   provided HTML element, using those imported via
   Google Fonts.
*/
function chooseFont(element) {
    fontList = [
        'ibm-plex-serif-regular', 
        'special-elite-regular',
        'baskervville-medium',
        'fredericka-the-great-regular',
        'charis-sil-regular-italic'
    ]
    const randomFactor = Math.random();
    const index = Math.floor(randomFactor * fontList.length); 
    element.classList.add(fontList[index]);
}

/* runAnimations() changes opacities of select elements
   to load in the quote and auxiliary information.
*/
function runAnimations() {
    const quoteElement = document.getElementById('quote');
    quoteElement.classList.remove("opacity-0");
    quoteElement.classList.add("opacity-100");

    const corners = document.querySelectorAll('.corner');
    corners.forEach(element => {
        element.classList.remove("opacity-0");
        element.classList.add("opacity-100");
    });

    const parentHeight = document.getElementById('quote-box').offsetHeight;
    console.log(parentHeight);
    const hrOne = document.getElementById('hr-top');
    const hrTwo = document.getElementById('hr-bottom');

    hrOne.style.transform = `translateY(-${parentHeight * 0.5}px)`;
    hrOne.classList.remove("opacity-0");
    hrOne.classList.add("opacity-100");
    hrTwo.style.transform = `translateY(${parentHeight * 0.5}px)`;
    hrTwo.classList.remove("opacity-0");
    hrTwo.classList.add("opacity-100");
    
}