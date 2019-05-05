import React, { PropTypes } from "react";
import { ResponsiveBar } from "@nivo/bar";
import numeral from "numeral";

import ChartController from "./ChartController";

const SummaryChart = ({
  data,
  product_lines,
  years,
  distincts,
  startYear,
  endYear,
  onChangeEndYear,
  onChangeStartYear
}) => (
  <div className="card">
    <div className="card-body">
      <h5 className="card-title">Premium Earned</h5>
      <h6 className="card-subtitle mb-2 text-muted">From Each Product Line</h6>
      <ChartController
        distincts={distincts}
        startYear={startYear}
        endYear={endYear}
        onChangeEndYear={onChangeEndYear}
        onChangeStartYear={onChangeStartYear}
      />
      <div id="summary-bar-chart" style={{ height: 400 }}>
        <ResponsiveBar
          data={data}
          keys={product_lines}
          indexBy="year"
          margin={{
            top: 50,
            right: 130,
            bottom: 50,
            left: 60
          }}
          padding={0.3}
          colors={{
            scheme: "nivo"
          }}
          borderColor={{
            from: "color",
            modifiers: [["darker", 1.6]]
          }}
          axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Year",
            legendPosition: "middle",
            legendOffset: 32
          }}
          axisLeft={{
            format: v => `${numeral(v).format("(0a)")}`,
            tickSize: 1,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Premium Earned",
            legendPosition: "middle",
            legendOffset: -45
          }}
          label={d => `${d.id}: ${numeral(d.value).format("(0.00a)")}`}
          labelSkipWidth={12}
          labelSkipHeight={12}
          labelTextColor={{
            from: "color",
            modifiers: [["darker", 1.6]]
          }}
          legends={[
            {
              dataFrom: "keys",
              anchor: "bottom-right",
              direction: "column",
              justify: false,
              translateX: 120,
              translateY: 0,
              itemsSpacing: 2,
              itemWidth: 100,
              itemHeight: 20,
              itemDirection: "left-to-right",
              itemOpacity: 0.85,
              symbolSize: 20,
              effects: [
                {
                  on: "hover",
                  style: {
                    itemOpacity: 1
                  }
                }
              ]
            }
          ]}
          animate={true}
          motionStiffness={90}
          motionDamping={15}
        />
      </div>
    </div>
  </div>
);

export default SummaryChart;
