// Function to generate the calendar
function generateCalendar() {
    const calendarContainer = document.getElementById('calendar');
    const header = document.getElementById('currentMonthYear');

    // Get current date
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    // Set the header to display the current month and year
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    header.textContent = `${monthNames[currentMonth]} ${currentYear}`;

    // Get the first day of the month and total days in the month
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    const totalDays = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Clear previous content
    calendarContainer.innerHTML = '';

    // Display days of the week (Mon to Sun) at the top starting with Sunday
    const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    for (const day of daysOfWeek) {
        const dayElement = document.createElement('div');
        dayElement.className = 'day';
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
        dayElement.className = 'day';

        // Create a link for each day
        const dayLink = document.createElement('a');
        dayLink.textContent = dayCount;
        dayLink.href = `javascript:openModalPopup(${currentYear}, ${currentMonth + 1}, ${dayCount})`;

        dayElement.appendChild(dayLink);
        calendarContainer.appendChild(dayElement);
    }
}

// Function to open the modal in a new popup window with only the date in the URL
function openModalPopup(year, month, day) {
    console.log(`openModalPopup called with year=${year}, month=${month}, day=${day}`);

    // Calculate the position to center the modal
    const leftPosition = (window.innerWidth - 600) / 2;
    const topPosition = (window.innerHeight - 400) / 2;

    const url = `/popup_modal?year=${year}&month=${month}&day=${day}`;
    console.log(`URL: ${url}`);
    window.open(url, 'Modal', `height=400,width=600,left=${leftPosition},top=${topPosition}`);
}

// Function to close the modal
function closeModal() {
    window.close();
}

// Call the function to generate the initial calendar
generateCalendar();
