import { useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend
} from "recharts";

const API_URL = "/api";

function App() {

  const [businessId, setBusinessId] = useState("");
  const [assets, setAssets] = useState([]);
  const [underutilized, setUnderutilized] = useState([]);
  const [maintenanceAlerts, setMaintenanceAlerts] = useState([]);

  const [newAsset, setNewAsset] = useState({
    asset_name: "",
    category: "",
    location: "",
    department: "",
    daily_operating_hours: "",
    hourly_run_cost: "",
    maintenance_threshold: ""
  });

  const COLORS = ["#0088FE","#00C49F","#FFBB28","#FF8042"];

  const categories = ["Electronics","Machinery","Vehicles","IT Equipment"];
  const departments = ["IT","Operations","Manufacturing","Admin"];
  const locations = ["Office","Warehouse","Factory Floor"];

  const generateAssetCode = () => {
    if (assets.length === 0) return "A001";

    const numbers = assets.map(a =>
      parseInt(a.asset_code.replace("A",""))
    );

    const max = Math.max(...numbers);
    return "A" + String(max + 1).padStart(3,"0");
  };

  const fetchAssets = async () => {

    if (!businessId) {
      alert("Enter Business ID");
      return;
    }

    const response = await fetch(
      `${API_URL}/assets?business_id=${businessId}`
    );

    const data = await response.json();

    setAssets(data);

    fetchUnderutilized();
    fetchMaintenanceAlerts();
  };

  const fetchUnderutilized = async () => {

    const response = await fetch(
      `${API_URL}/underutilized-assets?business_id=${businessId}`
    );

    const data = await response.json();

    setUnderutilized(data);
  };

  const fetchMaintenanceAlerts = async () => {

    const response = await fetch(
      `${API_URL}/maintenance-alerts?business_id=${businessId}`
    );

    const data = await response.json();

    setMaintenanceAlerts(data);
  };

  const handleInputChange = (e) => {
    setNewAsset({
      ...newAsset,
      [e.target.name]: e.target.value
    });
  };

  const addAsset = async () => {

    const assetCode = generateAssetCode();

    await fetch(
      `${API_URL}/assets?business_id=${businessId}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...newAsset,
          asset_code: assetCode,
          daily_operating_hours: Number(newAsset.daily_operating_hours),
          hourly_run_cost: Number(newAsset.hourly_run_cost),
          maintenance_threshold: Number(newAsset.maintenance_threshold)
        })
      }
    );

    fetchAssets();

    setNewAsset({
      asset_name: "",
      category: "",
      location: "",
      department: "",
      daily_operating_hours: "",
      hourly_run_cost: "",
      maintenance_threshold: ""
    });
  };

  const totalAssets = assets.length;
  const underutilizedCount = underutilized.length;
  const maintenanceCount = maintenanceAlerts.length;

  const totalOperatingCost = assets.reduce((sum, asset) => {
    return sum + (asset.hourly_run_cost || 0);
  }, 0);

  const categoryData = Object.values(
    assets.reduce((acc, asset) => {
      if (!acc[asset.category]) {
        acc[asset.category] = { name: asset.category, value: 0 };
      }
      acc[asset.category].value += 1;
      return acc;
    }, {})
  );

  const usageData = assets.map(asset => ({
    name: asset.asset_name,
    hours: asset.daily_operating_hours || 0
  }));

  return (
    <div style={{ padding:40, fontFamily:"Arial", background:"#f5f6fa", minHeight:"100vh" }}>

      <h1>Inventory Management System</h1>

      <div style={{display:"flex",gap:20,marginBottom:40}}>
        <div style={{background:"white",padding:20,width:200}}>
          <h4>Total Assets</h4>
          <h2>{totalAssets}</h2>
        </div>

        <div style={{background:"white",padding:20,width:200}}>
          <h4>Underutilized</h4>
          <h2>{underutilizedCount}</h2>
        </div>

        <div style={{background:"white",padding:20,width:200}}>
          <h4>Maintenance Alerts</h4>
          <h2>{maintenanceCount}</h2>
        </div>

        <div style={{background:"white",padding:20,width:200}}>
          <h4>Total Hourly Cost</h4>
          <h2>${totalOperatingCost}</h2>
        </div>
      </div>

      <div style={{marginBottom:30}}>
        <input
          placeholder="Enter Business ID"
          value={businessId}
          onChange={(e)=>setBusinessId(e.target.value)}
        />
        <button onClick={fetchAssets}>Load Dashboard</button>
      </div>

      <div style={{display:"flex",gap:40,marginBottom:40}}>
        <div style={{background:"white",padding:20}}>
          <h3>Asset Category Distribution</h3>
          <PieChart width={300} height={250}>
            <Pie data={categoryData} dataKey="value" nameKey="name" outerRadius={80}>
              {categoryData.map((entry,index)=>(
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip/>
          </PieChart>
        </div>

        <div style={{background:"white",padding:20}}>
          <h3>Daily Usage Hours</h3>
          <BarChart width={400} height={250} data={usageData}>
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="name"/>
            <YAxis/>
            <Tooltip/>
            <Legend/>
            <Bar dataKey="hours" fill="#8884d8"/>
          </BarChart>
        </div>
      </div>

      <div style={{background:"white",padding:20,marginBottom:30}}>
        <h2>Add Asset</h2>

        <input name="asset_name" placeholder="Asset Name" value={newAsset.asset_name} onChange={handleInputChange} />

        <select name="category" value={newAsset.category} onChange={handleInputChange}>
          <option value="">Select Category</option>
          {categories.map(c => <option key={c}>{c}</option>)}
        </select>

        <select name="department" value={newAsset.department} onChange={handleInputChange}>
          <option value="">Select Department</option>
          {departments.map(d => <option key={d}>{d}</option>)}
        </select>

        <select name="location" value={newAsset.location} onChange={handleInputChange}>
          <option value="">Select Location</option>
          {locations.map(l => <option key={l}>{l}</option>)}
        </select>

        <input name="daily_operating_hours" placeholder="Daily Hours" value={newAsset.daily_operating_hours} onChange={handleInputChange} />
        <input name="hourly_run_cost" placeholder="Hourly Cost" value={newAsset.hourly_run_cost} onChange={handleInputChange} />
        <input name="maintenance_threshold" placeholder="Maintenance Threshold" value={newAsset.maintenance_threshold} onChange={handleInputChange} />

        <button onClick={addAsset}>Add Asset</button>
      </div>

    </div>
  );
}

export default App;