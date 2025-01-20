# CL Flask CleverApp til Studering af Matematik

## Introduktion
Dette er en Flask-baseret webapp designet til at hjælpe brugere med at studere matematik på en interaktiv måde. Appen indeholder forskellige læringsmoduler, der fokuserer på forskellige emner inden for matematik, som integraler, sandsynlighed og normalfordeling.

Appen bruger matematiske visualiseringer, dynamiske eksempler og detaljerede forklaringer for at gøre læring sjov og engagerende. Projektet er åbent for samarbejde, og denne README giver retningslinjer for at arbejde sammen effektivt.

## Indholdsfortegnelse
- [Installation](#installation)
- [Brug af GitHub til Samarbejde](#brug-af-github-til-samarbejde)
- [Hvordan Man Laver Nye Sider](#hvordan-man-laver-nye-sider)
- [Arbejde med Layoutet](#arbejde-med-layoutet)
- [Oprettelse af Tooltip og Textbokse](#oprettelse-af-tooltip-og-textbokse)
- [Licens](#licens)

## Installation

### 1. Klon repository
Start med at klone repository:

```bash
git clone https://github.com/OskarAllerslev/CL
```
### 2. Installer nødvendige pakker
Efter at have klonet repository, naviger til projektmappen og installer de nødvendige afhængigheder:

```bash
pip install -r requirements.txt
```

Dette vil installere alle de nødvendige pakker, der er opført i requirements.txt filen.

### 3. Kør appen
For at køre appen, kan du blot køre følgende kommando:

```bash
python app.py
```
Appen vil være tilgængelig i din browser på http://127.0.0.1:5000/.


## Brug af GitHub til Samarbejde
For at arbejde sammen på dette projekt, følg disse trin:

### Fork repository:

Gå til GitHub-siden og klik på Fork knappen i øverste højre hjørne for at oprette en kopi af repository under din konto.
Klon din fork:

### Klon din fork til din lokale maskine:

```bash
git clone https://github.com/YOUR_USERNAME/CL.git
```
### Opret en ny gren:

For at undgå konflikter, opret en ny gren til dit arbejde:

```bash
git checkout -b your-branch-name
```
### Lav dine ændringer:

Rediger eller tilføj filer, som nødvendigt. For eksempel kan du ændre HTML-skabeloner, CSS-stilarter eller Python-kode.
Commit dine ændringer:

Efter at have lavet ændringer, commit dem:

```bash
git add .
git commit -m "Beskrivelse af dine ændringer"
```
Push dine ændringer:

Push ændringerne til din fork på GitHub:

```bash
git push origin your-branch-name
```
Opret en pull request:

Gå til din fork på GitHub og klik på New Pull Request knappen for at foreslå dine ændringer til det oprindelige projekt.
Hvordan Man Laver Nye Sider
For at lave en ny side, følg disse trin:

### Opret en ny HTML-fil:

Opret en ny HTML-fil i templates/ mappen, for eksempel new_page.html.
Udvid den basale skabelon:

I din nye HTML-fil, udvid den basale layout (som vist i de andre HTML-filer):

```html
{% extends "base.html" %}
```
#### Definer en titel og indhold:

Tilføj en titel og definer indholdssektionen:

```html
{% block title %}Ny Side Titel{% endblock %}

{% block content %}
<h1>Indhold af den Nye Side</h1>
{% endblock %}
```
Tilføj en rute i app.py:

I app.py, opret en ny rute for din side:

```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```
Tilføj et link i sidebar:

For at gøre den nye side tilgængelig, tilføj et link til sidebar i base.html:

```html
<li><a class="nav-link" href="/new-page">Ny Side</a></li>
```
Arbejde med Layoutet
Layoutet af siderne bruger base.html filen, som definerer den fælles struktur, herunder en sidebar til navigation og en footer. For at oprette en side med et konsekvent layout:

Sidebar:

Sidebaren indeholder links til de forskellige moduler. Hvert modul svarer til en side, som integraler eller sandsynlighed.
Tilføj links til nye sider i sidebar ved at følge strukturen, som er brugt i integraler.html, probability_intro.html osv.
Indhold:

Indeni hver sides content blok kan du tilføje HTML-indhold som tekst, formler, interaktive elementer og billeder. For eksempel:

```html
<div class="container mt-5">
    <h1>Emne Titel</h1>
    <p>Forklaring og eksempler.</p>
</div>
```
### Mathjax:

For at vise matematiske formler, brug Mathjax til at rendere LaTeX. Indpak din LaTeX kode i \[...\] for display matematik:

```html
<p>
    Formlen for integralet er:
    \[
    \int_a^b f(x) \, dx
    \]
</p>
```
### Oprettelse af Tooltip og Textbokse
Du kan oprette tooltips og textbokse over tekst for at give ekstra information, som dette:

```html
<span class="textbox">
    \( a \in \mathbb{R} \)
    <span class="textbox box">
        \( a \) er den nedre grænse for integralet.
    </span>
</span>
```
Denne kode viser en textbox, når du holder musen over udtrykket.
