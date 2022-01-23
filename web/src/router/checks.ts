import router from "./router";
import { Route, NavigationGuardNext } from "vue-router";
import store from "../store";
const restrictedCheck = (to: Route, from: Route, next: NavigationGuardNext) => {
  if (store.getters.supabase.auth.user()) {
    next();
  } else {
    router.replace({
      name: "Landing",
      params: { errorCode: "103", previousPath: to.path },
    });
  }
};

const saveCheck = (to: Route, from: Route, next: NavigationGuardNext) => {
  console.log("TH");
  next(false);
  const answer = window.confirm(
    "Do you really want to leave? you have unsaved changes!"
  );
  if (answer) {
    next();
  } else {
    next(false);
  }
};

export { restrictedCheck, saveCheck };
