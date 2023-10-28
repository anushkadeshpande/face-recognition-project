import { useEffect, useState } from "react";
import { IonApp, setupIonicReact } from "@ionic/react";
import { onSnapshot, query, orderBy } from "firebase/firestore";
import { logDbRef } from "./Firebase";

import "@ionic/react/css/core.css";

import "@ionic/react/css/normalize.css";
import "@ionic/react/css/structure.css";
import "@ionic/react/css/typography.css";

import "@ionic/react/css/padding.css";
import "@ionic/react/css/float-elements.css";
import "@ionic/react/css/text-alignment.css";
import "@ionic/react/css/text-transformation.css";
import "@ionic/react/css/flex-utils.css";
import "@ionic/react/css/display.css";

import "./theme/variables.css";
import axios from "axios";
import { PushNotifications } from "@capacitor/push-notifications";
import Home from "./pages/Home";
import "./App.css";

setupIonicReact();

const App = () => {
  const [logsData, setLogsData] = useState([]);

  useEffect(() => {
    const register = () => {
      PushNotifications.register();
      PushNotifications.addListener("registration", (token) => {
        sendDevice(token.value);
        getData();
      });
    };

    var sendDevice = (token) => {
      var headers = {
        "Content-Type": "application/json; charset=utf-8",
      };

      axios({
        method: "post",
        baseURL: "https://onesignal.com",
        url: "/api/v1/players",
        port: 443,
        headers: headers,
        data: {
          app_id: "0a807065-20b8-4c43-a875-50bc94fd049f",
          included_segments: ["Active Users", "Subscribed Users"],
          identifier: token,
          device_type: 1,
        },
      }).catch((error) => {
        console.log(error);
      });
    };

    const getData = () => {
      const q = query(logDbRef, orderBy("Time", "asc"));

      onSnapshot(q, (querySnapshot) => {
        setLogsData([]);
        querySnapshot.forEach((doc) => {
          const docData = doc.data();
          docData.date = new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          }).format(docData.Time.toDate());
          docData.Time = new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
          }).format(docData.Time.toDate());
          setLogsData((prevData) => [docData, ...prevData]);
        });
      });
    };
    //register();
    getData()
  }, []);

  return (
    <IonApp>
      <Home logsData={logsData} />
    </IonApp>
  );
};

export default App;
