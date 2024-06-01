// Function to update the outcome list
function updateCallMain(data) {
    const outcomeList = document.querySelector('#outcome-list');
    outcomeList.innerHTML = ''; // Clear existing content

    for (const [status, ids] of Object.entries(data)) {
        const section = document.createElement('div');
        section.classList.add('outcome-section');

        const header = document.createElement('h4');
        header.textContent = `${status} (${ids.length})`;
        header.classList.add('outcome-header');
        header.onclick = () => {
            const content = section.querySelector('.outcome-content');
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        };

        const content = document.createElement('div');
        content.classList.add('outcome-content');
        content.style.display = 'none'; // Initially hidden

        const idList = document.createElement('ul');
        ids.forEach(id => {
            const listItem = document.createElement('li');
            listItem.textContent = id;
            idList.appendChild(listItem);
        });

        content.appendChild(idList);
        section.appendChild(header);
        section.appendChild(content);
        outcomeList.appendChild(section);
    }
}

function updateMainResults(split, model) {
    console.log(split);
    console.log(model);
    const url = `https://raw.githubusercontent.com/swe-bench/experiments/main/evaluation/${split}/${model}/results/results.json`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            updateCallMain(data);
        })
        .catch(error => {
            console.error('Error fetching the JSON data:', error);
        });
}

