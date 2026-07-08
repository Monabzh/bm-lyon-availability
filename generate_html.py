import json

with open("books.json", "r", encoding="utf-8") as f:
    books = json.load(f)

html_debut = """<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Disponibilité bibliothèque</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-table@1.27.3/dist/bootstrap-table.min.css">
    
  </head>
  <body>
    <table 
        id="table"
        data-toggle="table"
        data-search="true">
      <thead>
        <tr>
          <th>Titre</th>
          <th>Auteur</th>
          <th>Date</th>
          <th>
            <div class="d-flex gap-2 align-items-center">
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
                        Bibliothèques disponibles
                    </button>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">"""

all_branches = set()
for book in books:
    for branch in book["branches"]:
        all_branches.add(branch)
all_branches = sorted(all_branches)

for branch in all_branches:
    html_debut += f"<li><input type=\"checkbox\" class=\"btn-check biblio-check\" checked id=\"btncheck{all_branches.index(branch) + 1}\" autocomplete=\"on\" onChange=\"filterTable()\"><label class=\"btn btn-outline-primary\" for=\"btncheck{all_branches.index(branch) + 1}\">{branch}</label></li>"

html_int = """                </ul>
            </div>
                <div class="btn-group" role="group" aria-label="Basic radio toggle button group">
                    <input type="radio" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" checked onClick="radio()">
                    <label class="btn btn-outline-primary" for="btnradio1">Toutes les bibli</label>

                    <input type="radio" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" onClick="radio()">
                    <label class="btn btn-outline-primary" for="btnradio2">Mes bibli !</label>
                </div>
            </div>
        </th>
        </tr>
      </thead>
      <tbody>"""


html_lignes = ""
for book in books:
    branches = ", ".join(book["branches"]) if book["branches"] else "—"
    html_lignes += f"<tr><td>{book['title']}</td><td>{book['author']}</td><td>{book['date']}</td><td>{branches}</td></tr>\n"

html_fin ="""
      </tbody>
    </table>

    <script src="https://cdn.jsdelivr.net/npm/jquery@3.7.1/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap-table@1.27.3/dist/bootstrap-table.min.js"></script>
    <script>
        bootstrap.Dropdown.Default.popperConfig = { strategy:"fixed" };
    </script>

    <script>
        function filterTable() {
            var checkboxes = document.querySelectorAll('.biblio-check');
            var selectedLibraries = [];
            checkboxes.forEach(function(checkbox) {
                if (checkbox.checked) {
                    selectedLibraries.push(checkbox.nextElementSibling.textContent.trim());
                }
            });

            var rows = document.querySelectorAll('#table tbody tr');
            rows.forEach(function(row) {
                var librariesCell = row.cells[3].textContent;
                var isVisible = selectedLibraries.some(function(library) {
                    return librariesCell.includes(library);
                });
                row.style.display = isVisible ? 'table-row' : 'none';
            });
        }
    </script>

    <script>
        function radio() {
            var radio = document.querySelectorAll('input[name="btnradio"]:checked')[0];
            var checkboxes = document.querySelectorAll('.biblio-check');
            if (radio.id === "btnradio1") {
                checkboxes.forEach(function(checkbox) {
                    checkbox.checked = true;
                });
            } else {
                checkboxes.forEach(function(checkbox) {
                    var label = checkbox.nextElementSibling.textContent.trim();
                    checkbox.checked = label === "Part-Dieu" || label === "1e arrdt";
                });
            }
            filterTable();
        }
    </script>

    <script>
        bootstrap.Dropdown.Default.popperConfig = { strategy:"fixed" };
        setTimeout(function() { filterTable(); }, 0);
    </script>

  </body>
</html>"""

with open("index.html", "w") as f:
    f.write(html_debut + html_int + html_lignes + html_fin)