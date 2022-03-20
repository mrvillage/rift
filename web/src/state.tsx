import { SupabaseClient } from "@supabase/supabase-js";
import { useState } from "react";

const [state, setState] = useState({
  supabase: new SupabaseClient(
    import.meta.env.VITE_SUPABASE_URL,
    import.meta.env.VITE_SUPABASE_ANON_KEY
  ),
});

export default { state, setState };
