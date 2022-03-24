import {
  Group,
  Space,
  UnstyledButton,
  Text,
  useMantineTheme,
} from "@mantine/core";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
          color: theme.colors.dark[0],

          "&:hover": {
            backgroundColor: theme.colors.dark[6],
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
