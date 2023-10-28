import React, { useEffect } from "react";
import { Plugins, Capacitor } from "@capacitor/core";
import {
  IonContent,
  IonHeader,
  IonPage,
  IonThumbnail,
  IonTitle,
  IonToolbar,
  IonButton,
} from "@ionic/react";
//import ExploreContainer from '../components/ExploreContainer';
import "./Home.css";
import {
  IonModal,
  IonIcon,
  IonList,
  IonItem,
  IonLabel,
  IonImg,
  IonButtons,
  IonRippleEffect,
} from "@ionic/react";
import { useState } from "react";
import {
  closeOutline,
  informationCircleOutline,
  heart,
  closeCircleOutline,
} from "ionicons/icons";
import { StatusBar, Style } from "@capacitor/status-bar";

const Home = ({ logsData }) => {
  const [showModal, setShowModal] = useState(false);
  const [modalContent, setModalContent] = useState("");

  const [showInfoModal, setShowInfoModal] = useState(false);
  var today = new Date();
  today = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(today);
  let date = "None";
  StatusBar.setBackgroundColor({ color: "#ffffff" });
  StatusBar.setStyle({ style: Style.Light });

  const getDate = (currDate) => {
    let isChanged = false;
    if (date !== currDate) {
      isChanged = true;
    } else isChanged = false;

    return isChanged ? (date = currDate) : false;
  };

  return (
    <IonPage>
      <IonToolbar>
        <IonButtons mode="md" slot="start" className="ion-padding">
          <IonButton
            mode="md"
            style={{ "--background": "#FFF0EF" }}
            onClick={() => setShowInfoModal(true)}
          >
            <IonIcon
              mode="md"
              icon={informationCircleOutline}
              slot="icon-only"
              style={{ color: "#F16056", fontSize: "35px" }}
            />
          </IonButton>
        </IonButtons>

        <IonTitle mode="ios">
          <span style={{ color: "#5A5A5A", fontWeight: 800, fontSize: "20px" }}>
            Entry <span style={{ color: "#F16056" }}>Logs</span>
          </span>
        </IonTitle>
      </IonToolbar>
      <IonContent fullscreen>
        <div className="ion-padding list">
          {logsData.map((data, i) => (
            <div>
              <div className="date-divider">
                {getDate(data.date)
                  ? data.date === today
                    ? "Today"
                    : data.date
                  : ""}
              </div>

              <div
                class="item"
                key={i}
                button
                onClick={() => {
                  setShowModal(true);
                  setModalContent(data.Picture);
                }}
              >
                <img
                  src={data.Picture}
                  alt="pic"
                  height="100%"
                  className="img"
                ></img>

                <div
                  style={{
                    marginLeft: "10px",
                    fontWeight: 600,
                    color: "#F16056",
                  }}
                >
                  {data.Time}
                </div>
              </div>
            </div>
          ))}
        </div>
      </IonContent>

      <IonModal isOpen={showModal} className="picture-modal">
        <div className="modal-content">
          <img src={modalContent} />
          <button className="modalButton" onClick={() => setShowModal(false)}>
            <IonIcon
              icon={closeCircleOutline}
              style={{ color: "#F16056" }}
              className="circle-close-button"
            ></IonIcon>
          </button>
        </div>
      </IonModal>

      <IonModal isOpen={showInfoModal} className="info-modal">
        <div className="info-modal-content">
          <div className="info-page-content">
            <span className="info-header">
              Made with{" "}
              <IonIcon
                mode="md"
                icon={heart}
                slot="icon-only"
                style={{
                  color: "#F16056",
                  fontSize: "35px",
                }}
              />
              {"  "}
              by
            </span>
            <div className="sharinushka">
              <span className="our-name">Anushka Deshpande</span>
              <span className="our-roll-number">BI014</span>
            </div>
            <div className="sharinushka">
              <span className="our-name">Bhavini Patil</span>
              <span className="our-roll-number">BI018</span>
            </div>
            <div className="sharinushka">
              <span className="our-name">Sharayu Pisal</span>
              <span className="our-roll-number">BI067</span>
            </div>
            <button
              className="infoModalButton"
              onClick={() => setShowInfoModal(false)}
            >
              <IonIcon
                icon={closeCircleOutline}
                style={{ color: "#F16056" }}
                className="circle-close-button"
              ></IonIcon>
            </button>
          </div>
        </div>
      </IonModal>
    </IonPage>
  );
};

export default Home;
