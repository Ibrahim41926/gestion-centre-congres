import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Elementcentre: React.FC = () => {
  return (
    <div id="page-elementcentre-5">
    <div id="ih2i8q" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iqca07" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="im78n2" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iiwhiy" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i0xmv5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionnaire">{"Gestionnaire"}</a>
          <a id="iey4os" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="i2ppqi" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centredecongres">{"CentreDeCongres"}</a>
          <a id="i6yqu3" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/paiement">{"Paiement"}</a>
          <a id="i62r9f" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="iv33bt" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/elementcentre">{"ElementCentre"}</a>
          <a id="in8aqs" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"Materiel"}</a>
          <a id="i7sc42" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"Prestation"}</a>
          <a id="iwmib5" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/personnereferente">{"PersonneReferente"}</a>
          <a id="imx7sb" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/tarif">{"Tarif"}</a>
          <a id="iyj639" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponibilte">{"Indisponibilte"}</a>
          <a id="i23fyh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/contraintes">{"Contraintes"}</a>
          <a id="iipf9v" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reglelocation">{"RegleLocation"}</a>
        </div>
        <p id="i7j89f" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i54e7a" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ivlgpm" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"ElementCentre"}</h1>
        <p id="ithbu5" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage ElementCentre data"}</p>
        <TableBlock id="table-elementcentre-5" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ElementCentre List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Nom", "column_type": "field", "field": "nom", "type": "str", "required": true}, {"label": "Description", "column_type": "field", "field": "description", "type": "str", "required": true}, {"label": "CapaciteMax", "column_type": "field", "field": "capaciteMax", "type": "int", "required": true}], "formColumns": [{"column_type": "field", "field": "nom", "label": "nom", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "description", "label": "description", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "capaciteMax", "label": "capaciteMax", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "centredecongres_1", "field": "centredecongres_1", "lookup_field": "nom", "entity": "CentreDeCongres", "type": "str", "required": true}, {"column_type": "lookup", "path": "tarif_1", "field": "tarif_1", "lookup_field": "saison", "entity": "Tarif", "type": "list", "required": true}, {"column_type": "lookup", "path": "contraintes", "field": "contraintes", "lookup_field": "dureeMinimale", "entity": "Contraintes", "type": "str", "required": false}, {"column_type": "lookup", "path": "indisponibilte", "field": "indisponibilte", "lookup_field": "dateDebut", "entity": "Indisponibilte", "type": "list", "required": false}]}} dataBinding={{"entity": "ElementCentre", "endpoint": "/elementcentre/"}} />
      </main>
    </div>    </div>
  );
};

export default Elementcentre;
