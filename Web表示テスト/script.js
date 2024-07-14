document.getElementById('csvFileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) {
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        displayCSV(text);
    };
    reader.readAsText(file);
});

function displayCSV(csv) {
    const rows = csv.split('\n');
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');

    tableHeader.innerHTML = '';
    tableBody.innerHTML = '';

    rows.forEach((row, index) => {
        const cols = row.split(',');

        const tr = document.createElement('tr');
        cols.forEach(col => {
            const cell = document.createElement(index === 0 ? 'th' : 'td');
            cell.textContent = col.trim();
            tr.appendChild(cell);
        });

        if (index === 0) {
            tableHeader.appendChild(tr);
        } else {
            tableBody.appendChild(tr);
        }
    });
}
