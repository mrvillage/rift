import { Button, Navbar, Box, ScrollArea, Affix } from "@mantine/core";
import UserMenu from "./UserMenu";
import SideBarItems from "./SideBarItems";
import { useAppContext } from "../../context/AppContext";
import { useNotifications } from "@mantine/notifications";
import { Icon } from "../../utils";

interface SideBarProps {
  opened: boolean;
}

const SideBar = ({ opened }: SideBarProps) => {
  const { supabase, isSignedIn, setIsSignedIn } = useAppContext();
  const { showNotification } = useNotifications();
  const signIn = async () => {
    const { user, error } = await supabase.auth.signIn(
      { provider: "discord" },
      { redirectTo: "http://localhost:3000" }
    );
    if (error) {
      console.error(error);
      showNotification({
        message: "Something went wrong signing in!",
        color: "red",
        icon: <Icon.X />,
        style: { background: "red" },
      });
    }
    if (user) {
      setIsSignedIn(true);
    }
  };
  const SignInButton = () => {
    return (
      <Button
        fullWidth
        size="md"
        variant="filled"
        color="green"
        onClick={signIn}
      >
        Sign In
      </Button>
    );
  };
  return (
    <Navbar
      hiddenBreakpoint="sm"
      hidden={!opened}
      width={{ sm: 200, lg: 300 }}
      p="xs"
    >
      <Navbar.Section grow component={ScrollArea}>
        <SideBarItems />
      </Navbar.Section>
      <Navbar.Section>
        <Box
          sx={(theme) => ({
            paddingTop: theme.spacing.sm,
            borderTop: `1px solid ${
              theme.colorScheme === theme.colors.dark[4]
            }`,
          })}
        >
          {!isSignedIn ? <SignInButton /> : <UserMenu />}
        </Box>
      </Navbar.Section>
    </Navbar>
  );
};

export default SideBar;
