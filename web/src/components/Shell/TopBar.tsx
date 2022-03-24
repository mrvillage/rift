import {
  ActionIcon,
  Burger,
  Container,
  Group,
  Header,
  MediaQuery,
  useMantineColorScheme,
  useMantineTheme,
} from "@mantine/core";
import * as Icon from "react-feather";
import { themePick } from "../../utils";
import TopActionIcon from "./TopActionIcon";
import DiscordIcon from "./DiscordIcon";

interface TopBarProps {
  opened: boolean;
  setOpened: (opened: boolean) => void;
}
const TopBar = ({ opened, setOpened }: TopBarProps) => {
  const { toggleColorScheme } = useMantineColorScheme();
  const theme = useMantineTheme();
  return (
    <Header height={60}>
      <Group sx={{ height: "100%" }} px={20} position="apart">
        <Group>
          <MediaQuery largerThan="sm" styles={{ display: "none" }}>
            <Burger
              opened={opened}
              onClick={() => setOpened(!opened)}
              color={theme.colors.gray[6]}
              mr="xl"
            />
          </MediaQuery>
          <MediaQuery smallerThan="sm" styles={{ display: "none" }}>
            <Icon.Aperture size={24} color={theme.colors.gray[6]} />
          </MediaQuery>
        </Group>
        <Group>
          <TopActionIcon
            label="Discord"
            href="https://rift.mrvillage.dev/discord"
          >
            <DiscordIcon color={theme.colors.gray[6]} />
          </TopActionIcon>
          <TopActionIcon
            label="GitHub"
            href="https://rift.mrvillage.dev/github"
          >
            <Icon.GitHub size={24} color={theme.colors.gray[6]} />
          </TopActionIcon>
          <TopActionIcon label="Add Rift" href="https://rift.mrvillage.dev/get">
            <Icon.Plus color={theme.colors.gray[6]} />
          </TopActionIcon>
          <TopActionIcon
            label={themePick("Light Mode", "Dark Mode")}
            onClick={() => toggleColorScheme()}
          >
            {themePick(
              <Icon.Sun size={16} color={theme.colors.gray[6]} />,
              <Icon.Moon size={16} color={theme.colors.gray[6]} />
            )}
          </TopActionIcon>
        </Group>
      </Group>
    </Header>
  );
};

export default TopBar;
