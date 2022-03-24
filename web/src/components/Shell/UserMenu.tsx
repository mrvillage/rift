import { Menu, useMantineTheme } from "@mantine/core";
import { useMediaQuery } from "@mantine/hooks";
import { useAppContext } from "../../context/AppContext";
import { Icon } from "../../utils";
import UserButton from "./UserButton";

const UserMenu = () => {
  const { supabase, setIsSignedIn } = useAppContext();
  const theme = useMantineTheme();
  const mobile = useMediaQuery(`(max-width: ${theme.breakpoints.sm}px)`);
  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) {
      console.error(error);
    } else {
      setIsSignedIn(false);
    }
  };
  return (
    <Menu
      sx={{ width: "100%" }}
      position={mobile ? "top" : "right"}
      placement={mobile ? "center" : "end"}
      control={<UserButton />}
    >
      <Menu.Label>Account</Menu.Label>
      <Menu.Item icon={<Icon.User size={mobile ? 30 : 15} />}>
        Profile
      </Menu.Item>
      <Menu.Item icon={<Icon.Settings size={mobile ? 30 : 15} />}>
        User Settings
      </Menu.Item>
      <Menu.Item
        icon={<Icon.LogOut size={mobile ? 30 : 15} />}
        onClick={signOut}
      >
        Logout
      </Menu.Item>
    </Menu>
  );
};

export default UserMenu;
