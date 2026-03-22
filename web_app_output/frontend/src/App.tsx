import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Gestionnaire from "./pages/Gestionnaire";
import Tarif from "./pages/Tarif";
import Indisponibilte from "./pages/Indisponibilte";
import Contraintes from "./pages/Contraintes";
import Reglelocation from "./pages/Reglelocation";
import Reservation from "./pages/Reservation";
import Centredecongres from "./pages/Centredecongres";
import Paiement from "./pages/Paiement";
import Evenement from "./pages/Evenement";
import Elementcentre from "./pages/Elementcentre";
import Materiel from "./pages/Materiel";
import Prestation from "./pages/Prestation";
import Personnereferente from "./pages/Personnereferente";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/gestionnaire" element={<Gestionnaire />} />
            <Route path="/tarif" element={<Tarif />} />
            <Route path="/indisponibilte" element={<Indisponibilte />} />
            <Route path="/contraintes" element={<Contraintes />} />
            <Route path="/reglelocation" element={<Reglelocation />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/centredecongres" element={<Centredecongres />} />
            <Route path="/paiement" element={<Paiement />} />
            <Route path="/evenement" element={<Evenement />} />
            <Route path="/elementcentre" element={<Elementcentre />} />
            <Route path="/materiel" element={<Materiel />} />
            <Route path="/prestation" element={<Prestation />} />
            <Route path="/personnereferente" element={<Personnereferente />} />
            <Route path="/" element={<Navigate to="/gestionnaire" replace />} />
            <Route path="*" element={<Navigate to="/gestionnaire" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
