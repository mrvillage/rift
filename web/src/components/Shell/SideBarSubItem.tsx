import {
  Group,
  Space,
  UnstyledButton,
  Text,
  useMantineTheme,
} from "@mantine/core";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { themePick } from "../../utils";
export interface SideBarSubItemProps {
  label: string;
  path: string;
}

const SideBarSubItem = ({ label, path }: SideBarSubItemProps) => {
  const [clicked, setClicked] = useState(false);
  const navigate = useNavigate();
  const theme = useMantineTheme();
  return (
    <Group direction="row" noWrap>
      <Space w="xs" />
      <UnstyledButton
        sx={{
          display: "block",
          width: "100%",
          padding: theme.spacing.xs,
          borderRadius: theme.radius.sm,
          color: themePick(theme.colors.dark[0], theme.black),
          "&:hover": {
            backgroundColor: themePick(
              theme.colors.dark[6],
              theme.colors.gray[0]
            ),
          },
        }}
        onClick={() => {
          setClicked(!clicked);
          if (path) {
            navigate(path);
          }
        }}
      >
        <Text size="sm">{label}</Text>
      </UnstyledButton>
    </Group>
  );
};

export default SideBarSubItem;
