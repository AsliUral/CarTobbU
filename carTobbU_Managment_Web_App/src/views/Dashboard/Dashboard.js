import React, { useState, useEffect } from 'react';
// react plugin for creating charts
import ChartistGraph from "react-chartist";
// @material-ui/core
import { makeStyles } from "@material-ui/core/styles";
import Update from "@material-ui/icons/Update";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import Accessibility from "@material-ui/icons/Accessibility";

// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";


import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";

const useStyles = makeStyles(styles);

export default function Dashboard(props) {
  const { dailySalesChart, emailsSubscriptionChart, completedTasksChartYDB, completedTasksChartTM, completedTasksChartMid, emailsSubscriptionChartTM } = props;
  const classes = useStyles();
  const [daysTobb, setdaysTobb] = useState(null);
  var Chartist = require("chartist");

  var delays = 80,
    durations = 500;
  var delays2 = 80,
    durations2 = 500;

  if (dailySalesChart != null) {
    return (
      <div>
        <GridContainer>
          <GridItem xs={12} sm={6} md={3}>
            <Card>
              <CardHeader color="info" stats icon>
                <CardIcon color="info">
                  <Accessibility />
                </CardIcon>
                <p className={classes.cardCategory}>CarTobbU Uygulamasını Kullanan Kişi Sayısı</p>
                <h3 className={classes.cardTitle}>+5</h3>
              </CardHeader>
              <CardFooter stats>
                <div className={classes.stats}>
                  <Update />
                  Just Updated
                </div>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
        <GridContainer>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="info">
                <ChartistGraph
                  className="ct-chart"
                  data={dailySalesChart.data}
                  type="Line"
                  options={dailySalesChart.options}
                  listener={dailySalesChart.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={classes.cardTitle}>Tobb Etu Haftalık Otopark Doluluk Oranı</h4>
                <p className={classes.cardCategory}>
                  <span className={classes.successText}>
                    <ArrowUpward className={classes.upArrowCardCategory} /> 55%
                  </span>{" "}
                  increase in today
                </p>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="warning">
                <ChartistGraph
                  className="ct-chart"
                  data={emailsSubscriptionChart.data}
                  type="Bar"
                  options={emailsSubscriptionChart.options}
                  responsiveOptions={emailsSubscriptionChart.responsiveOptions}
                  listener={emailsSubscriptionChart.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={classes.cardTitle}>Yabancı Diller Otopark Saatlik Doluluk Oranı</h4>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="danger">
                <ChartistGraph
                  className="ct-chart"
                  data={emailsSubscriptionChartTM.data}
                  type="Bar"
                  options={emailsSubscriptionChartTM.options}
                  responsiveOptions={emailsSubscriptionChartTM.responsiveOptions}
                  listener={emailsSubscriptionChartTM.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={classes.cardTitle}>Teknoloji Merkezi Otopark Saatlik Doluluk Oranı</h4>
              </CardBody>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="info">
                <ChartistGraph
                  className="ct-chart"
                  data={completedTasksChartYDB.data}
                  type="Line"
                  options={completedTasksChartYDB.options}
                  listener={completedTasksChartYDB.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={classes.cardTitle}>Yabancı Diller Otopark</h4>
              </CardBody>
              <CardFooter chart>
                <div className={classes.stats}>
                </div>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="warning">
                <ChartistGraph
                  className="ct-chart"
                  data={completedTasksChartTM.data}
                  type="Line"
                  options={completedTasksChartTM.options}
                  listener={completedTasksChartTM.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={classes.cardTitle}>Teknoloji Merkezi Otopark</h4>
              </CardBody>
              <CardFooter chart>
                <div className={classes.stats}>
                </div>
              </CardFooter>
            </Card>
          </GridItem>
          <GridItem xs={12} sm={12} md={4}>
            <Card chart>
              <CardHeader color="danger">
                <ChartistGraph
                  className="ct-chart"
                  data={completedTasksChartMid.data}
                  type="Line"
                  options={completedTasksChartMid.options}
                  listener={completedTasksChartMid.animation}
                />
              </CardHeader>
              <CardBody>
                <h4 className={classes.cardTitle}>Ara Otopark</h4>
                <p className={classes.cardCategory}></p>
              </CardBody>
              <CardFooter chart>
                <div className={classes.stats}>
                </div>
              </CardFooter>
            </Card>
          </GridItem>
        </GridContainer>
      </div>
    );
  } else {
    return null;
  }

}
