document.addEventListener("DOMContentLoaded", function() {
    function createHeader() {
        const headerHTML = `
        <!-- Bootstrap Navbar -->
        <nav class="navbar navbar-expand-lg bg-primary" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">CabinetCalc</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarColor01">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="/">Home
                            <span class="visually-hidden">(current)</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/login">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/estimate">Estimate</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/materials">Materials List</a>
                    </li>
                    
                </ul>
            </div>
        </div>
    </nav>
        `;
        document.getElementById('header-container').innerHTML = headerHTML;
    }

    createHeader();
});


