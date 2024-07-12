function generateCalendar() {
    const calendarContainer = document.getElementById('calendar');
    const header = document.getElementById('currentMonthYear');

    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const monthNames = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
    header.textContent = `${currentYear}년 ${monthNames[currentMonth]}`;

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    const totalDays = new Date(currentYear, currentMonth + 1, 0).getDate();

    calendarContainer.innerHTML = '';

    const daysOfWeek = ['일', '월', '화', '수', '목', '금', '토'];
    for (const day of daysOfWeek) {
        const dayElement = document.createElement('div');
        dayElement.className = 'day day-name';
        dayElement.textContent = day;
        calendarContainer.appendChild(dayElement);
    }

    for (let i = 0; i < firstDayOfMonth; i++) {
        const emptyDayElement = document.createElement('div');
        emptyDayElement.className = 'day empty-day';
        calendarContainer.appendChild(emptyDayElement);
    }

    for (let dayCount = 1; dayCount <= totalDays; dayCount++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'day day-number';

        const dayLink = document.createElement('a');
        dayLink.textContent = dayCount;
        dayLink.href = `javascript:openModalPopup(${currentYear}, ${currentMonth + 1}, ${dayCount})`;

        dayElement.appendChild(dayLink);
        calendarContainer.appendChild(dayElement);
    }
}

function openModalPopup(year, month, day) {
    $.get(`/inquiry/popup_modal/?year=${year}&month=${month}&day=${day}`, function(data) {
        $('#modalContent').html(data);
        $('#modalContainer').show();
    });
}

function closeModal() {
    $('#modalContainer').hide();
}

$(document).ready(function() {
    generateCalendar();
});
