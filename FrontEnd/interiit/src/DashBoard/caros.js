import React, { useRef, useState } from "react";
import { Chart } from "react-google-charts";
// Import Swiper React components
import { Swiper, SwiperSlide } from "swiper/react";
// import "./caros.scoped.css"
// Import Swiper styles
import "swiper/css";
import "swiper/css/effect-fade";
import "swiper/css/navigation";
import "swiper/css/pagination";

// import "./styles.css";

// import required modules
import { EffectFade, Navigation, Pagination } from "swiper";

export default function App({ ...props }) {
  let dataTorender = props.data;
  return (
    <>
      <Swiper
        effect={"fade"}
        navigation={true}
        pagination={{
          clickable: true,
        }}
        modules={[EffectFade, Navigation, Pagination]}
        className="mySwiper"
      >
        {dataTorender
          ? dataTorender.map((elem) => (
              <SwiperSlide>
                <div style={{paddingBottom:"20px"}}>
                  <Chart
                    chartType="Line"
                    data={elem}
                    style={{paddingTop:"20px"}}
                    options={{
                      title: elem[0][1],

                      curveType: "function",
                      height: "200px",
                      legend: { position: "bottom" },
                      interpolateNulls: true,
                    }}
                  />
                </div>
              </SwiperSlide>
            ))
          : null}
        {/* <SwiperSlide>
          <img src="https://swiperjs.com/demos/images/nature-1.jpg" />
        </SwiperSlide>
        <SwiperSlide>
          <img src="https://swiperjs.com/demos/images/nature-2.jpg" />
        </SwiperSlide>
        <SwiperSlide>
          <img src="https://swiperjs.com/demos/images/nature-3.jpg" />
        </SwiperSlide>
        <SwiperSlide>
          <img src="https://swiperjs.com/demos/images/nature-4.jpg" />
        </SwiperSlide> */}
      </Swiper>
    </>
  );
}
