function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitle.innerText = films[i].title == films[i].title_ru ? ''  : films[i].title;
            tdTitleRus.innerText = films[i].title_ru;
            tdYear.innerText = films[i].year;

            let editButton = document.createElement('button');
            editButton.innerText = 'Редактировать';

            let delButton = document.createElement('button');
            delButton.innerText = 'Удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            }

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitle);
            tr.append(tdTitleRus);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}" из списка?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector("div.modal").style.display = "none";
  }

function cancel() {
hideModal();
}

function addFilm() {
document.getElementById("id").value = "";
document.getElementById("title").value = "";
document.getElementById("title-ru").value = "";
document.getElementById("year").value = "";
document.getElementById("description").value = "";
showModal();
}

function sendFilm() {
    const film = {
      title: document.getElementById("title").value,
      title_ru: document.getElementById("title-ru").value,
      year: document.getElementById("year").value,
      description: document.getElementById("description").value,
    };
    const url = "/lab7/rest-api/films/";
    const method = "POST";
    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(film),
    }).then(function () {
      fillFilmList();
      hideModal();
    });
  }