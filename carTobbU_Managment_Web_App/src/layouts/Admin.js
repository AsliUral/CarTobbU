import React, { useState, useEffect } from 'react';
import { Switch, Route, Redirect } from "react-router-dom";
// creates a beautiful scrollbar
import PerfectScrollbar from "perfect-scrollbar";
import "perfect-scrollbar/css/perfect-scrollbar.css";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

import Menu from "components/Navbars/Menu.js";
import Dashboard from "views/Dashboard/Dashboard.js";

import routes from "routes.js";

import styles from "assets/jss/material-dashboard-react/layouts/adminStyle.js";

import bgImage from "assets/img/sidebar-2.jpg";
import logo from "assets/img/reactlogo.png";
import Penalties from "../components/Penalties/Penalties.js"
import { Container, Header, List } from "semantic-ui-react";

import data from './data.json';

let ps;
const switchRoutes = (
  <Switch>
    {routes.map((prop, key) => {
      if (prop.layout === "/admin") {
        return (
          <Route
            path={prop.layout + prop.path}
            component={prop.component}
            key={key}
          />
        );
      }
      return null;
    })}
    <Redirect from="/admin" to="/admin/dashboard" />
  </Switch>
);

const useStyles = makeStyles(styles);

export default function Admin({ ...rest }) {
  // styles
  const classes = useStyles();
  // ref to help us initialize PerfectScrollbar on windows devices
  const mainPanel = React.createRef();
  // states and functions
  const [image, setImage] = React.useState(bgImage);
  const [color, setColor] = React.useState("blue");
  const [fixedClasses, setFixedClasses] = React.useState("dropdown show");
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const [auth, setAuth] = React.useState(false);

  const [penaltyOpen, setpenaltyOpen] = React.useState(false);
  const [dashboardOpen, setDashboardOpen] = React.useState(false);
  const [list, setData] = React.useState(null);
  const [error, setError] = React.useState(null);

  var Chartist = require("chartist");
  var delays = 80,
    durations = 500;
  var delays2 = 80,
    durations2 = 500;

  var doc = null;
  var dataTobb = null;
  var tobb = [];
  var dailySalesChart = null;
  var emailsSubscriptionChart = null;
  var emailsSubscriptionChartTM = null;
  tobb = data;
  var hoursbyDay = null;
  var hoursbyDayTM = null;
  var daysTobbParkingLotYDB = null;
  var daysTobbParkingLotTM = null;
  var daysTobbParkingLotMid = null;
  var completedTasksChartYDB = null;
  var completedTasksChartTM = null;
  var completedTasksChartMid = null;

  calculateDaysOfWeek(tobb);
  parkingSlotDaysOccupancy(tobb, "YDB Car Park", "Monday");
  parkingSlotDaysOccupancyTM(tobb, "TM Car Park", "Monday");


  var ydb = Math.floor(Math.random() * 155) + 1;
  var m = Math.floor(Math.random() * 113) + 1;
  var tm = Math.floor(Math.random() * 315) + 1;

  popularparkingSlotDaysOccupancyYDB(tobb, "Y" + ydb);
  popularparkingSlotDaysOccupancyTM(tobb, "T" + tm);
  popularparkingSlotDaysOccupancyMid(tobb, "M" + m);

  function calculateDaysOfWeek(tobb) {
    var M = 0;
    var Tu = 0;
    var W = 0;
    var Th = 0;
    var F = 0;
    var Sa = 0;
    var Su = 0;
    tobb.forEach(function (data) {
      if (data.Day === "Monday") {
        if (data.ParkingLotStatus === "Occupied") {
          M = M + 1;
        }
      } else if (data.Day === "Tuesday") {
        if (data.ParkingLotStatus === "Occupied") {
          Tu = Tu + 1;
        }
      } else if (data.Day === "Wednesday") {
        if (data.ParkingLotStatus === "Occupied") {
          W = W + 1;
        }
      } else if (data.Day === "Thursday") {
        if (data.ParkingLotStatus === "Occupied") {
          Th = Th + 1;
        }
      } else if (data.Day === "Friday") {
        if (data.ParkingLotStatus === "Occupied") {
          F = F + 1;
        }
      } else if (data.Day === "Saturday") {
        if (data.ParkingLotStatus === "Occupied") {
          Sa = Sa + 1;
        }
      } else if (data.Day == "Sunday") {
        if (data.ParkingLotStatus === "Occupied") {
          Su = Su + 1;
        }
      }
    });
    var temp = { Monday: M, Tuesday: Tu, Wednesday: W, Thursday: Th, Friday: F, Saturday: Sa, Sunday: Su };

    dailySalesChart = {
      data: {
        labels: ["M", "T", "W", "T", "F", "S", "S"],
        series: [[temp.Monday, temp.Tuesday, temp.Wednesday, temp.Thursday, temp.Friday, temp.Saturday, temp.Sunday]]
      },
      options: {
        lineSmooth: Chartist.Interpolation.cardinal({
          tension: 0
        }),
        low: 0,
        high: 8000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
        chartPadding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        }
      },
      // for animation
      animation: {
        draw: function (data) {
          if (data.type === "line" || data.type === "area") {
            data.element.animate({
              d: {
                begin: 600,
                dur: 700,
                from: data.path
                  .clone()
                  .scale(1, 0)
                  .translate(0, data.chartRect.height())
                  .stringify(),
                to: data.path.clone().stringify(),
                easing: Chartist.Svg.Easing.easeOutQuint
              }
            });
          } else if (data.type === "point") {
            data.element.animate({
              opacity: {
                begin: (data.index + 1) * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: "ease"
              }
            });
          }
        }
      }
    };

  }

  function parkingSlotDaysOccupancy(tobb, ParkZoneName, Day) {
    var eight = 0;
    var nine = 0;
    var ten = 0;
    var eleven = 0;
    var twelve = 0;
    var thirteen = 0;
    var fourteen = 0;
    var fifteen = 0;
    var sixteen = 0;
    var seventeen = 0;
    var eighteen = 0;
    var nineteen = 0;
    tobb.forEach(function (data) {
      if (data.ParkZoneName === ParkZoneName) {
        if (data.Day === Day) {
          if (data.ParkingLotStatus === "Occupied") {
            if (data.Hour == "08-00-00") {
              eight = eight + 1;
            } else if (data.Hour == "09-00-00") {
              nine = nine + 1;
            } else if (data.Hour == "10-00-00") {
              ten = ten + 1;
            } else if (data.Hour == "11-00-00") {
              eleven = eleven + 1;
            } else if (data.Hour == "12-00-00") {
              twelve = twelve + 1;
            } else if (data.Hour == "13-00-00") {
              thirteen = thirteen + 1;
            } else if (data.Hour == "14-00-00") {
              fourteen = fourteen + 1;
            } else if (data.Hour == "15-00-00") {
              fifteen = fifteen + 1;
            } else if (data.Hour == "16-00-00") {
              sixteen = sixteen + 1;
            } else if (data.Hour == "17-00-00") {
              seventeen = seventeen + 1;
            } else if (data.Hour == "18-00-00") {
              eighteen = eighteen + 1;
            } else if (data.Hour == "19-00-00") {
              nineteen = nineteen + 1;
            }
          }
        }
      }
    });
    hoursbyDay = { eight: eight, nine: nine, ten: ten, eleven: eleven, twelve: twelve, thirteen: thirteen, fourteen: fourteen, fifteen: fifteen, sixteen: sixteen, seventeen: seventeen, eighteen: eighteen, nineteen: nineteen };

    emailsSubscriptionChart = {
      data: {
        labels: [
          "08.00",
          "09.00",
          "10.00",
          "11.00",
          "12.00",
          "13.00",
          "14.00",
          "15.00",
          "16.00",
          "17.00",
          "18.00",
          "19.00"
        ],
        series: [[hoursbyDay.eight, hoursbyDay.nine, hoursbyDay.ten, hoursbyDay.eleven, hoursbyDay.twelve, hoursbyDay.thirteen, hoursbyDay.fourteen, hoursbyDay.fifteen, hoursbyDay.sixteen, hoursbyDay.seventeen, hoursbyDay.eighteen, hoursbyDay.nineteen]]
      },
      options: {
        axisX: {
          showGrid: false
        },
        low: 0,
        high: 600,
        chartPadding: {
          top: 0,
          right: 5,
          bottom: 0,
          left: 0
        }
      },
      responsiveOptions: [
        [
          "screen and (max-width: 640px)",
          {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }
        ]
      ],
      animation: {
        draw: function (data) {
          if (data.type === "bar") {
            data.element.animate({
              opacity: {
                begin: (data.index + 1) * delays2,
                dur: durations2,
                from: 0,
                to: 1,
                easing: "ease"
              }
            });
          }
        }
      }
    };
  }

  function parkingSlotDaysOccupancyTM(tobb, ParkZoneName, Day) {
    var eight = 0;
    var nine = 0;
    var ten = 0;
    var eleven = 0;
    var twelve = 0;
    var thirteen = 0;
    var fourteen = 0;
    var fifteen = 0;
    var sixteen = 0;
    var seventeen = 0;
    var eighteen = 0;
    var nineteen = 0;
    tobb.forEach(function (data) {
      if (data.ParkZoneName === ParkZoneName) {
        if (data.Day === Day) {
          if (data.ParkingLotStatus === "Occupied") {
            if (data.Hour == "08-00-00") {
              eight = eight + 1;
            } else if (data.Hour == "09-00-00") {
              nine = nine + 1;
            } else if (data.Hour == "10-00-00") {
              ten = ten + 1;
            } else if (data.Hour == "11-00-00") {
              eleven = eleven + 1;
            } else if (data.Hour == "12-00-00") {
              twelve = twelve + 1;
            } else if (data.Hour == "13-00-00") {
              thirteen = thirteen + 1;
            } else if (data.Hour == "14-00-00") {
              fourteen = fourteen + 1;
            } else if (data.Hour == "15-00-00") {
              fifteen = fifteen + 1;
            } else if (data.Hour == "16-00-00") {
              sixteen = sixteen + 1;
            } else if (data.Hour == "17-00-00") {
              seventeen = seventeen + 1;
            } else if (data.Hour == "18-00-00") {
              eighteen = eighteen + 1;
            } else if (data.Hour == "19-00-00") {
              nineteen = nineteen + 1;
            }
          }
        }
      }
    });
    hoursbyDayTM = { eight: eight, nine: nine, ten: ten, eleven: eleven, twelve: twelve, thirteen: thirteen, fourteen: fourteen, fifteen: fifteen, sixteen: sixteen, seventeen: seventeen, eighteen: eighteen, nineteen: nineteen };

    emailsSubscriptionChartTM = {
      data: {
        labels: [
          "08.00",
          "09.00",
          "10.00",
          "11.00",
          "12.00",
          "13.00",
          "14.00",
          "15.00",
          "16.00",
          "17.00",
          "18.00",
          "19.00"
        ],
        series: [[hoursbyDayTM.eight, hoursbyDayTM.nine, hoursbyDayTM.ten, hoursbyDayTM.eleven, hoursbyDayTM.twelve, hoursbyDayTM.thirteen, hoursbyDayTM.fourteen, hoursbyDayTM.fifteen, hoursbyDayTM.sixteen, hoursbyDayTM.seventeen, hoursbyDayTM.eighteen, hoursbyDayTM.nineteen]]
      },
      options: {
        axisX: {
          showGrid: false
        },
        low: 0,
        high: 600,
        chartPadding: {
          top: 0,
          right: 5,
          bottom: 0,
          left: 0
        }
      },
      responsiveOptions: [
        [
          "screen and (max-width: 640px)",
          {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }
        ]
      ],
      animation: {
        draw: function (data) {
          if (data.type === "bar") {
            data.element.animate({
              opacity: {
                begin: (data.index + 1) * delays2,
                dur: durations2,
                from: 0,
                to: 1,
                easing: "ease"
              }
            });
          }
        }
      }
    };
  }

  function popularparkingSlotDaysOccupancyYDB(tobb, ParkingLot) {
    var M = 0;
    var Tu = 0;
    var W = 0;
    var Th = 0;
    var F = 0;
    var Sa = 0;
    var Su = 0;
    tobb.forEach(function (data) {
      if (data.Day === "Monday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            M = M + 1;
          }
        }
      } else if (data.Day === "Tuesday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Tu = Tu + 1;
          }
        }
      } else if (data.Day === "Wednesday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            W = W + 1;
          }
        }
      } else if (data.Day === "Thursday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Th = Th + 1;
          }
        }
      } else if (data.Day === "Friday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            F = F + 1;
          }
        }
      } else if (data.Day === "Saturday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Sa = Sa + 1;
          }
        }
      } else if (data.Day == "Sunday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Su = Su + 1;
          }
        }
      }
    });
    daysTobbParkingLotYDB = { Monday: M, Tuesday: Tu, Wednesday: W, Thursday: Th, Friday: F, Saturday: Sa, Sunday: Su };

    completedTasksChartYDB = {
      data: {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        series: [[daysTobbParkingLotYDB.Monday, daysTobbParkingLotYDB.Tuesday, daysTobbParkingLotYDB.Wednesday, daysTobbParkingLotYDB.Thursday, daysTobbParkingLotYDB.Friday, daysTobbParkingLotYDB.Saturday, daysTobbParkingLotYDB.Sunday]]
      },
      options: {
        lineSmooth: Chartist.Interpolation.cardinal({
          tension: 0
        }),
        low: 0,
        high: 40, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
        chartPadding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        }
      },
      animation: {
        draw: function (data) {
          if (data.type === "line" || data.type === "area") {
            data.element.animate({
              d: {
                begin: 600,
                dur: 700,
                from: data.path
                  .clone()
                  .scale(1, 0)
                  .translate(0, data.chartRect.height())
                  .stringify(),
                to: data.path.clone().stringify(),
                easing: Chartist.Svg.Easing.easeOutQuint
              }
            });
          } else if (data.type === "point") {
            data.element.animate({
              opacity: {
                begin: (data.index + 1) * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: "ease"
              }
            });
          }
        }
      }
    };

  }

  function popularparkingSlotDaysOccupancyTM(tobb, ParkingLot) {
    var M = 0;
    var Tu = 0;
    var W = 0;
    var Th = 0;
    var F = 0;
    var Sa = 0;
    var Su = 0;
    tobb.forEach(function (data) {
      if (data.Day === "Monday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            M = M + 1;
          }
        }
      } else if (data.Day === "Tuesday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Tu = Tu + 1;
          }
        }
      } else if (data.Day === "Wednesday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            W = W + 1;
          }
        }
      } else if (data.Day === "Thursday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Th = Th + 1;
          }
        }
      } else if (data.Day === "Friday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            F = F + 1;
          }
        }
      } else if (data.Day === "Saturday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Sa = Sa + 1;
          }
        }
      } else if (data.Day == "Sunday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Su = Su + 1;
          }
        }
      }
    });
    daysTobbParkingLotTM = { Monday: M, Tuesday: Tu, Wednesday: W, Thursday: Th, Friday: F, Saturday: Sa, Sunday: Su };

    completedTasksChartTM = {
      data: {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        series: [[daysTobbParkingLotTM.Monday, daysTobbParkingLotTM.Tuesday, daysTobbParkingLotTM.Wednesday, daysTobbParkingLotTM.Thursday, daysTobbParkingLotTM.Friday, daysTobbParkingLotTM.Saturday, daysTobbParkingLotTM.Sunday]]
      },
      options: {
        lineSmooth: Chartist.Interpolation.cardinal({
          tension: 0
        }),
        low: 0,
        high: 40, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
        chartPadding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        }
      },
      animation: {
        draw: function (data) {
          if (data.type === "line" || data.type === "area") {
            data.element.animate({
              d: {
                begin: 600,
                dur: 700,
                from: data.path
                  .clone()
                  .scale(1, 0)
                  .translate(0, data.chartRect.height())
                  .stringify(),
                to: data.path.clone().stringify(),
                easing: Chartist.Svg.Easing.easeOutQuint
              }
            });
          } else if (data.type === "point") {
            data.element.animate({
              opacity: {
                begin: (data.index + 1) * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: "ease"
              }
            });
          }
        }
      }
    };

  }
  function popularparkingSlotDaysOccupancyMid(tobb, ParkingLot) {
    var M = 0;
    var Tu = 0;
    var W = 0;
    var Th = 0;
    var F = 0;
    var Sa = 0;
    var Su = 0;
    tobb.forEach(function (data) {
      if (data.Day === "Monday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            M = M + 1;
          }
        }
      } else if (data.Day === "Tuesday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Tu = Tu + 1;
          }
        }
      } else if (data.Day === "Wednesday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            W = W + 1;
          }
        }
      } else if (data.Day === "Thursday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Th = Th + 1;
          }
        }
      } else if (data.Day === "Friday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            F = F + 1;
          }
        }
      } else if (data.Day === "Saturday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Sa = Sa + 1;
          }
        }
      } else if (data.Day == "Sunday") {
        if (data.ParkingLotStatus === "Occupied") {
          if (data.ParkingLot === ParkingLot) {
            Su = Su + 1;
          }
        }
      }
    });
    daysTobbParkingLotMid = { Monday: M, Tuesday: Tu, Wednesday: W, Thursday: Th, Friday: F, Saturday: Sa, Sunday: Su };

    completedTasksChartMid = {
      data: {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        series: [[daysTobbParkingLotMid.Monday, daysTobbParkingLotMid.Tuesday, daysTobbParkingLotMid.Wednesday, daysTobbParkingLotMid.Thursday, daysTobbParkingLotMid.Friday, daysTobbParkingLotMid.Saturday, daysTobbParkingLotMid.Sunday]]
      },
      options: {
        lineSmooth: Chartist.Interpolation.cardinal({
          tension: 0
        }),
        low: 0,
        high: 40, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
        chartPadding: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        }
      },
      animation: {
        draw: function (data) {
          if (data.type === "line" || data.type === "area") {
            data.element.animate({
              d: {
                begin: 600,
                dur: 700,
                from: data.path
                  .clone()
                  .scale(1, 0)
                  .translate(0, data.chartRect.height())
                  .stringify(),
                to: data.path.clone().stringify(),
                easing: Chartist.Svg.Easing.easeOutQuint
              }
            });
          } else if (data.type === "point") {
            data.element.animate({
              opacity: {
                begin: (data.index + 1) * delays,
                dur: durations,
                from: 0,
                to: 1,
                easing: "ease"
              }
            });
          }
        }
      }
    };

  }
  const handleImageClick = image => {
    setImage(image);
  };
  const handleColorClick = color => {
    setColor(color);
  };
  const handleLogin = () => {
    console.log("beni cagirdiniz");
    //useHttpListCall();
    setAuth(true);
  };
  const handleFixedClick = () => {
    if (fixedClasses === "dropdown") {
      setFixedClasses("dropdown show");
    } else {
      setFixedClasses("dropdown");
    }
  };
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  const getRoute = () => {
    return window.location.pathname !== "/admin/maps";
  };
  const resizeFunction = () => {
    if (window.innerWidth >= 960) {
      setMobileOpen(false);
    }
  };
  const styleLink = document.createElement("link");
  styleLink.rel = "stylesheet";
  styleLink.href = "https://cdn.jsdelivr.net/npm/semantic-ui/dist/semantic.min.css";
  document.head.appendChild(styleLink);
  return (
    <>
      <Menu routes={routes} auth={auth}
        handleLogin={handleLogin}
        penaltyOpen={penaltyOpen} setpenaltyOpen={setpenaltyOpen}
        dashboardOpen={dashboardOpen} setDashboardOpen={setDashboardOpen}
        {...rest}
      >
        {getRoute() ? (
          <div className={classes.content}>
            <div className={classes.container}>{switchRoutes}</div>
          </div>
        ) : (
            <div className={classes.map}>{switchRoutes}</div>
          )}
      </Menu >
      {penaltyOpen && !dashboardOpen ? (
        <Penalties>
        </Penalties>
      ) : (
          <Dashboard dailySalesChart={dailySalesChart}
            emailsSubscriptionChart={emailsSubscriptionChart}
            emailsSubscriptionChartTM={emailsSubscriptionChartTM}
            completedTasksChartYDB={completedTasksChartYDB}
            completedTasksChartTM={completedTasksChartTM}
            completedTasksChartMid={completedTasksChartMid}
          >

          </Dashboard>
        )}
    </>
  );
}
