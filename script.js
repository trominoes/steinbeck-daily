// script.js


// Function to calculate the number of days since January 1, 2026
function calculateDaysSince(date) {
    const now = new Date();
    const startDate = new Date(date);
    const difference = now - startDate; // in milliseconds
    return Math.floor(difference / (1000 * 60 * 60 * 24)); // converting to days
}

// Set the value to the days counter
const daysCounterElement = document.getElementById('days-counter');
const daysSince = calculateDaysSince("2026-01-01");
daysCounterElement.innerText = `${daysSince} days`;

// Array of quotes
const quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
    "In the middle of difficulty lies opportunity. - Albert Einstein",
    "It always seems impossible until it’s done. - Nelson Mandela"
];

// Function to select a random quote
function getRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    return quotes[randomIndex];
}

// Display random quote
const quoteElement = document.getElementById('quote');
quoteElement.innerText = getRandomQuote();
