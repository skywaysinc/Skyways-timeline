export default async function handler(req, res) {
  const PAT = process.env.AIRTABLE_PAT;
  const BASE_ID = process.env.AIRTABLE_BASE_ID;
  const TABLE_IDS = ['tblqPi1dUtTjK1bhk', 'tblb3eu5LS3aD9zVi', 'tblrijmejajlssqh5', 'tblD3LBp0p2m562Oc'];

  if (!PAT || !BASE_ID) {
    return res.status(500).json({ error: 'Missing Airtable credentials in server environment.' });
  }

  try {
    let allRecordsCount = 0;
    let totalFlightHours = 0;
    
    // Omni-Fetch across all specific flight tables in the aerospace database
    for (const tableId of TABLE_IDS) {
      let offset = null;
      let keepFetching = true;

      while (keepFetching) {
        // Omitting specific field filtering to safely handle missing 'Flight time (h)' columns gracefully across varying tables
        const url = `https://api.airtable.com/v0/${BASE_ID}/${tableId}?` + 
                    (offset ? `offset=${offset}` : 'pageSize=100');
                    
        const response = await fetch(url, {
          headers: {
            'Authorization': `Bearer ${PAT}`
          }
        });

        if (!response.ok) {
          keepFetching = false;
          break;
        }

        const data = await response.json();
        allRecordsCount += (data.records || []).length;
        
        (data.records || []).forEach(record => {
          totalFlightHours += (record.fields['Flight time (h)'] || 0);
        });

        if (data.offset) {
          offset = data.offset;
        } else {
          keepFetching = false;
        }
      }
    }

    return res.status(200).json({ 
       globalFlights: allRecordsCount,
       flightHours: Math.round(totalFlightHours),
       status: "success" 
    });

  } catch (e) {
     return res.status(500).json({ error: e.message });
  }
}
