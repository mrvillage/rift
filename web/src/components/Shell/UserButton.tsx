import { Avatar, Box, Group, Text, UnstyledButton } from "@mantine/core";
import { forwardRef } from "react";
import * as Icon from "react-feather";
import { themePick } from "../../utils";

const UserButton = forwardRef<HTMLButtonElement>(({ ...others }, ref) => (
  <UnstyledButton
    ref={ref}
    sx={(theme) => ({
      display: "block",
      width: "100%",
      padding: theme.spacing.xs,
      borderRadius: theme.radius.sm,
      color: themePick(theme.colors.dark[0], theme.black),
      "&:hover": {
        backgroundColor: themePick(theme.colors.dark[6], theme.colors.gray[0]),
      },
    })}
    {...others}
  >
    <Group>
      <Avatar
        src="https://cdn.discordapp.com/avatars/258298021266063360/a_09ca45f2e171fdcd29425ee29a671977.gif?size=4096"
        radius="xl"
      />
      <Box sx={{ flex: 1 }}>
        <Text size="sm" weight={500}>
          Village
        </Text>
        <Text size="xs" color="dimmed">
          #0001
        </Text>
      </Box>

      <Icon.ChevronRight size={18} />
    </Group>
  </UnstyledButton>
));

export default UserButton;
