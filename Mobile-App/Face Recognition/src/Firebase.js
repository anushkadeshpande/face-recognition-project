import { initializeApp } from "firebase/app";
import { getFirestore, collection} from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyAKjEridGdtvblGovd-nKbJlwlVM8bM2YM",
  authDomain: "face-recognition-29af2.firebaseapp.com",
  projectId: "face-recognition-29af2",
  storageBucket: "face-recognition-29af2.appspot.com",
  messagingSenderId: "576253162873",
  appId: "1:576253162873:web:2550dffef848ea629caba8"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const logDbRef = collection(db, "Logs");
export { db, logDbRef };