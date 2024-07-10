// script.js
// Initialize Firebase
// firebase.initializeApp({
//     // Your Firebase configuration here
// });

const startButton = $('.start-button'); // Use jQuery selector
startButton.on('click', () => { // Use jQuery's 'on' method for event listeners
    // Generate a correlationID
    const correlationID = generateCorrelationID();

    // Create a document in Firestore (or mock)
    fetch('/create_retrospective', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ correlationID: correlationID })
    })
    .then(response => {
        if (response.ok) {
            // Redirect to /level.html with correlationID
            window.location.href = `/level.html?correlationID=${correlationID}`;
        } else {
            console.error("Error creating retrospective: ", response.status);
        }
    })
    .catch(error => {
        console.error("Error adding document: ", error);
    });
});

function generateCorrelationID() {
    // Implement your correlationID generation logic here
    // Example: using a random string
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

// Function to delete the correlationID and redirect to home
function deleteCorrelationIDAndRedirect() {
    const correlationID = new URLSearchParams(window.location.search).get('correlationID');

    if (correlationID) {

        // Check if FLASK_ENV is set to 'development'
        if (window.FLASK_ENV === 'development') {
            // Use mock_firestore.py
            const db = new MockFirestore(); // Assuming MockFirestore is defined globally
            console.log(`Deleting document with correlationID: ${correlationID} (MockFirestore)`);
            db.collection('retrospectives').doc(correlationID).delete()
                .then(() => {
                    console.log(`Document with correlationID: ${correlationID} deleted (MockFirestore)`);
                    window.location.href = '/';
                })
                .catch(error => {
                    console.error("Error deleting document: ", error);
                });
        };
    }
         
}

// Attach the deleteCorrelationIDAndRedirect function to the home button
$('.home-button').on('click', deleteCorrelationIDAndRedirect);