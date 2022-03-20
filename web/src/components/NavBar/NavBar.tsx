import { Error } from "../Error";
import { Button, Typography } from "@supabase/ui";
import { useContext, useState } from "react";
import { Link } from "react-router-dom";
import state from "../../state";

const NavBar = () => {
  const [showing, setShowing] = useState(false);
  const signIn = async () => {
    try {
      // const { error } = await state.supabase.auth.signIn({
      // provider: "discord",
      // });
      setShowing(!showing);
    } catch (error) {
      console.error(error);
      setShowing(true);
    }
  };

  return (
    <>
      <Button
        size="xlarge"
        style={{ backgroundColor: "Transparent" }}
        shadow={false}
      >
        <Link to="/">
          <Typography.Text>Home</Typography.Text>
        </Link>
      </Button>
      <Button
        size="xlarge"
        style={{ backgroundColor: "Transparent" }}
        onClick={signIn}
        shadow={false}
      >
        <Typography.Text>Sign In</Typography.Text>
      </Button>
      {showing && (
        <Error
          title="Something went wrong signing in!"
          showing={showing}
          setShowing={setShowing}
        ></Error>
      )}
    </>
  );
};

export default NavBar;
