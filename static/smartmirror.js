
// Function to generate the calendar
function generateCalendar() {
    const calendarContainer = document.getElementById('calendar');
    const header = document.getElementById('currentMonthYear');

    // Get current date
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    // Set the header to display the current month and year
    const monthNames = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
    header.textContent = `${currentYear + "년"} ${monthNames[currentMonth]}`;

    // Get the first day of the month and total days in the month
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    const totalDays = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Clear previous content
    calendarContainer.innerHTML = '';

    // Display days of the week (Mon to Sun) at the top starting with Sunday
    const daysOfWeek = ['일', '월', '화', '수', '목', '금', '토'];
    for (const day of daysOfWeek) {
        const dayElement = document.createElement('div');
        dayElement.className = 'day day-name';
        dayElement.textContent = day;
        calendarContainer.appendChild(dayElement);
    }

    // Adjust the position of the first day of the month
    for (let i = 0; i < firstDayOfMonth; i++) {
        const emptyDayElement = document.createElement('div');
        emptyDayElement.className = 'day empty-day';
        calendarContainer.appendChild(emptyDayElement);
    }

    // Display days of the month as clickable links
    for (let dayCount = 1; dayCount <= totalDays; dayCount++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'day day-number';
        
        // Create a link for each day
        const dayLink = document.createElement('a');
        dayLink.textContent = dayCount;
        dayLink.href = `javascript:showModal(${currentYear}, ${currentMonth + 1}, ${dayCount})`;

        dayElement.appendChild(dayLink);
        calendarContainer.appendChild(dayElement);
    }
}

// Function to show the modal
function showModal(year, month, day) {
    const uid = document.getElementById('uid').value;
    const url = `/smartmirror/inquiry/popup_modal/?year=${year}&month=${month}&day=${day}&uid=${uid}`;

    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById('modalContainer').innerHTML = data;
            document.getElementById('modalContainer').style.display = 'block';
        })
        .catch(error => console.error('Error fetching modal:', error));
}


// Function to close the modal
function closeModal() {
    document.getElementById('modalContainer').style.display = 'none';
}

// Initialize the calendar when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', (event) => {
    generateCalendar();
});
