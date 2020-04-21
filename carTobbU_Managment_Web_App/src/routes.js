
import Dashboard from "@material-ui/icons/Dashboard";
// core components/views for Admin layout
import DashboardPage from "views/Dashboard/Dashboard.js";


const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: Dashboard,
    component: DashboardPage,
    layout: "/admin"
  }
];

export default dashboardRoutes;
