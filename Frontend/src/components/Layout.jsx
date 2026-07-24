import { Link, NavLink, Outlet } from 'react-router-dom';

function Layout() {
  return (
    <div className="app-shell">
      <div className="container">
        <header className="crud-header">
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <h1>AI SERVICE DESK</h1>
          </Link>
        </header>

        <div className="crud-layout">
          <aside className="crud-sidebar">
            <div className="panel-title" style={{ marginBottom: '16px', paddingBottom: '8px', borderBottom: '1px solid var(--border)' }}>
              Navigation
            </div>
            <nav className="nav-menu">
              <NavLink to="/" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                Create Ticket
              </NavLink>
              <NavLink to="/tickets" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                Search Tickets
              </NavLink>
            </nav>
          </aside>

          <main className="crud-main">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}

export default Layout;
